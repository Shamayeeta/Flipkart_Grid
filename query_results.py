from collections import Counter
from string import punctuation
import numpy as np
import requests
from tqdm import tqdm
from collections import defaultdict
from pprint import pprint
import pandas as pd
from SimilarityFinder import SimilarityFinder
from heapq import heappop, heappush, heapify
import random

def search_results(results, name):
    queries = {"top": [],"bottom": [],"coverall": [],"onepiece": [], "accessories": [], "footwear": []}
    cats = ["top","bottom","coverall","onepiece", "accessories", "footwear"]

    for cat in cats:
        if cat in results:
            for item in results[cat]:
                queries[cat].append(item)

    occasions = ""
    if "occasion" in results:
        for item in results["occasion"]:
            occasions += "+" + item

    seasons = ""
    if "seasons" in results:
        for item in results["seasons"]:
            seasons += "+" + item

    for i in queries:
        for j in queries[i]:
            j += occasions

    users = pd.read_pickle('users.pkl')
    name = name[1:]
    user = users.loc[users['FirstName'] == name]
    gender = ""
    products_user = { "productsBoughtUser" : [] 
                    , "productsViewedUser" : []
                    , "productsWishlistUser" : []}
    totalproducts_user = 0
    if not user.empty:
        if user.iloc[0]["Gender"] == "F":
            gender = "Female"
        elif user.iloc[0]["Gender"] == "M":
            gender = "Male"
        for i in queries:
            for j in queries[i]:
                j += gender
                
        totalproducts_user = len(user.iloc[0]["ProductsBought"]) + len(user.iloc[0]["ProductsViewedInLast30Days"]) + len(user.iloc[0]["ProductsInWishlist"])

        if totalproducts_user > 15  :
            if len(user.iloc[0]["ProductsViewedInLast30Days"]) < 7:
                products_user["productsViewedUser"] = user.iloc[0]["ProductsViewedInLast30Days"]
            else:
                products_user["productsViewedUser"] = random.sample(user.iloc[0]["ProductsViewedInLast30Days"],6)
            if len(user.iloc[0]["ProductsBought"]) < 6:
                products_user["productsBoughtUser"] = user.iloc[0]["ProductsBought"]
            else:
                products_user["productsBoughtUser"] = random.sample(user.iloc[0]["ProductsBought"],5)
            if len(user.iloc[0]["ProductsInWishlist"]) < 5:
                products_user["productsWishlistUser"] = user.iloc[0]["ProductsInWishlist"]
            else:
                products_user["productsWishlistUser"] = random.sample(user.iloc[0]["ProductsInWishlist"],4)
        else:
            products_user["productsViewedUser"] = user.iloc[0]["ProductsViewedInLast30Days"]
            products_user["productsBoughtUser"] = user.iloc[0]["ProductsBought"]
            products_user["productsWishlistUser"] = user.iloc[0]["ProductsInWishlist"]

    pprint(products_user)

    search_results = {}
    for i in queries:
        for j in queries[i]:
            response = requests.get(f"https://flipkart-scraper-api.dvishal485.workers.dev/search/{j}").json()
            total_search_results = response["total_result"]
            search_products = response["result"]
            ranked_products = similarity_ranker(search_products, products_user, totalproducts_user)
            if i not in search_results:
                search_results[i] = [ranked_products]
            else:
                search_results[i].append(ranked_products)
    return search_results


def similarity_ranker(search_products, products_user, totalproducts_user):
    if len(products_user["productsViewedUser"]) + len(products_user["productsBoughtUser"]) + len(products_user["productsWishlistUser"]) == 0:
        ans = []
        for i in search_products:
            ans.append((0,i["name"], i["link"]))
        return ans
    check = SimilarityFinder('sentence-transformers/all-mpnet-base-v2')
    heap = []
    heapify(heap)
    weights = { "productsViewedUser" : 0.5, "productsBoughtUser" : 0.3, "productsWishlistUser": 0.2}
    if len(search_products) > 10:
        search_products = search_products[2:12]
    for i in search_products:
        val = 0
        for cat in products_user:
            for j in products_user[cat]:
                val += weights[cat]*check.calculate_similarity(
                check.calculate_embeddings(str(j[1])),
                check.calculate_embeddings(i["name"])).item()
        sim = val/min(20, totalproducts_user)
        heappush(heap, (-sim , i["name"], i["link"]))

        sorted_tuples = []
        max_heap = heap
        while max_heap:
            max_value_neg, value, link = heappop(max_heap)
            sorted_tuples.append((abs(max_value_neg), value, link))

        return sorted_tuples
