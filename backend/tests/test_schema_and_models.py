from decimal import Decimal

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import engine
from app.modules.catalog.models import (
    Brand,
    Category,
    Product,
    ProductImage,
    ProductVariant,
)
from app.modules.users.models import User, UserRole


def test_expected_tables_exist():
    inspector = inspect(engine)
    tables = set(inspector.get_table_names())
    expected = {
        "alembic_version",
        "users",
        "brands",
        "categories",
        "products",
        "product_categories",
        "product_images",
        "product_variants",
    }
    assert expected.issubset(tables)


def test_catalog_and_user_relationships_and_constraints():
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection)
        try:
            user = User(
                email="schema-test@example.com",
                hashed_password="hashed_password_placeholder",
                full_name="Schema Test User",
                role=UserRole.CUSTOMER,
            )
            brand = Brand(name="Schema Test Brand", slug="schema-test-brand")
            cat_cleanser = Category(name="Schema Cleansers", slug="schema-cleansers")
            cat_hydration = Category(name="Schema Hydration", slug="schema-hydration")

            product = Product(
                brand=brand,
                name="Hydrating Gel Cleanser",
                slug="hydrating-gel-cleanser",
                description="Gentle daily cleanser",
                ingredients="Water, Glycerin",
                skin_types=["dry", "sensitive"],
                skin_concerns=["dehydration"],
                benefits=["cleansing", "soothing"],
                categories=[cat_cleanser, cat_hydration],
            )
            ProductImage(
                product=product,
                url="https://example.com/cleanser.jpg",
                is_primary=True,
                sort_order=1,
            )
            ProductVariant(
                product=product,
                sku="TEST-SKU-50ML",
                name="50ml",
                price=Decimal("19.99"),
                stock=10,
            )

            session.add_all([user, brand, cat_cleanser, cat_hydration, product])
            session.flush()

            assert user.id is not None
            assert product.id is not None
            assert len(product.categories) == 2
            assert len(product.images) == 1
            assert len(product.variants) == 1
            assert product.average_rating == Decimal("0.00")

            with pytest.raises(IntegrityError):
                with session.begin_nested():
                    invalid_variant = ProductVariant(
                        product=product,
                        sku="TEST-SKU-INVALID",
                        name="Invalid Price",
                        price=Decimal("0.00"),
                        stock=5,
                    )
                    session.add(invalid_variant)
                    session.flush()
        finally:
            session.close()
            transaction.rollback()