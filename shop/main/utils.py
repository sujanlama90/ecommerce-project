import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count

from main.models import Product
from payments.models import OrderItem


def recommend_products_collab(user_id, top_n=5):

    # Step 1: Get user-product purchase data
    order_items = OrderItem.objects.filter().values(
        "order__user_id",
        "product_id"
    )

    if not order_items.exists():
        return Product.objects.all()[:top_n]

    # Step 2: Convert QuerySet to DataFrame
    df = pd.DataFrame(order_items)

    # Rename columns to make them easier to understand
    df = df.rename(columns={
        "order__user_id": "user_id"
    })

    # Step 3: Create user-product matrix
    user_product_matrix = pd.crosstab(
        df["user_id"],
        df["product_id"]
    )

    # Step 4: If current user has never purchased anything
    if user_id not in user_product_matrix.index:

        popular_products = (
            Product.objects
            .annotate(
                order_count=Count("orderitems")
            )
            .order_by("-order_count")[:top_n]
        )

        return popular_products

    # Step 5: Calculate similarity between users
    similarity = cosine_similarity(user_product_matrix)

    similarity_df = pd.DataFrame(
        similarity,
        index=user_product_matrix.index,
        columns=user_product_matrix.index
    )

    # Step 6: Find users similar to current user
    similar_users = (
        similarity_df[user_id]
        .sort_values(ascending=False)
        .index[1:]
    )

    # Step 7: Products already purchased by current user
    user_products = set(
        df[df["user_id"] == user_id]["product_id"]
    )

    recommendations = []

    # Step 8: Get products purchased by similar users
    for similar_user in similar_users:

        similar_user_products = set(
            df[df["user_id"] == similar_user]["product_id"]
        )

        # Remove products current user already purchased
        new_products = similar_user_products - user_products

        recommendations.extend(new_products)

        if len(recommendations) >= top_n:
            break

    # Step 9: Return recommended products
    return Product.objects.filter(
        id__in=recommendations[:top_n]
    )