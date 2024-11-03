import base64
import os
import time
from typing import Dict, List

from agori import ProcessingError, SecureChromaDB


def create_demo_collections(db: SecureChromaDB, collections_config: List[Dict]) -> None:
    """Create multiple collections with their respective documents."""
    for config in collections_config:
        try:
            collection = db.create_collection(
                name=config["name"], metadata=config["metadata"]
            )
            print(f"\nCreated collection: {collection.name}")

            db.add_documents(
                collection_name=collection.name,
                documents=config["documents"],
                metadatas=config["metadatas"],
            )
            print(f"Added {len(config['documents'])} documents to {collection.name}")
        except ProcessingError as e:
            print(f"Error processing collection {config['name']}: {str(e)}")


def query_collections(
    db: SecureChromaDB, collection_queries: Dict[str, List[str]]
) -> None:
    """Query multiple collections with their respective search terms."""
    for collection_name, queries in collection_queries.items():
        try:
            print(f"\nQuerying collection: {collection_name}")
            results = db.query_collection(
                collection_name=collection_name, query_texts=queries, n_results=2
            )

            print(f"Results for queries: {queries}")
            for i, docs in enumerate(results["documents"]):
                print(f"\nResults for query: '{queries[i]}'")
                for j, doc in enumerate(docs):
                    print(f"Document {j+1}: {doc}")
                    if "metadatas" in results and results["metadatas"]:
                        print(f"Metadata: {results['metadatas'][i][j]}")
                print(f"Similarity scores: {results['distances'][i]}")
        except ProcessingError as e:
            print(f"Error querying collection {collection_name}: {str(e)}")


def demonstrate_collection_management(db: SecureChromaDB) -> None:
    """Demonstrate collection management operations."""
    try:
        # List initial collections
        print("\nInitial collections:")
        initial_collections = db.list_collections()
        for collection in initial_collections:
            print(f"- {collection['name']}")

        # Drop a collection
        if initial_collections:
            collection_to_drop = initial_collections[0]["name"]
            print(f"\nDropping collection: {collection_to_drop}")
            db.drop_collection(collection_to_drop)

            # Verify collection was dropped
            updated_collections = db.list_collections()
            print("\nRemaining collections:")
            for collection in updated_collections:
                print(f"- {collection['name']}")

    except ProcessingError as e:
        print(f"Error in collection management: {str(e)}")


def main():
    try:
        # Generate encryption key
        encryption_key = base64.urlsafe_b64encode(os.urandom(32)).decode()

        # Initialize SecureChromaDB with context manager
        with SecureChromaDB(
            api_key="14a38573c7c04028af5e11f1e158ec71",
            api_endpoint="https://openaihumanvaluex.openai.azure.com/",
            encryption_key=encryption_key,
            db_unique_id="test_db_name",
            base_storage_path="./secure_storage",
            model_name="adaembedding",
            api_version="2024-02-15-preview",
            api_type="azure",
        ) as db:
            # Define multiple collections with their documents
            collections_config = [
                {
                    "name": "hr_documents",
                    "metadata": {
                        "description": "HR department documents",
                        "department": "Human Resources",
                        "security_level": "high",
                        "created_by": "admin",
                        "version": "1.0",
                    },
                    "documents": [
                        "Employee performance review 2023",
                        "Salary structure updates for Q2",
                        "New hire onboarding procedures",
                        "Employee benefits package 2024",
                        "HR policy updates March 2024",
                    ],
                    "metadatas": [
                        {"type": "review", "year": "2023", "confidential": "true"},
                        {"type": "compensation", "quarter": "Q2", "restricted": "true"},
                        {"type": "procedure", "category": "onboarding"},
                        {"type": "benefits", "year": "2024"},
                        {"type": "policy", "month": "March", "year": "2024"},
                    ],
                },
                {
                    "name": "finance_documents",
                    "metadata": {
                        "description": "Finance department documents",
                        "department": "Finance",
                        "security_level": "high",
                        "created_by": "finance_admin",
                        "version": "2.0",
                    },
                    "documents": [
                        "Q1 2024 Financial Report",
                        "Annual budget planning 2024",
                        "Investment strategy overview",
                        "Tax planning guidelines 2024",
                        "Quarterly revenue projections",
                    ],
                    "metadatas": [
                        {"type": "report", "period": "Q1_2024", "confidential": "true"},
                        {"type": "planning", "year": "2024"},
                        {"type": "strategy", "category": "investment"},
                        {"type": "guidelines", "year": "2024"},
                        {"type": "projections", "period": "Q2_2024"},
                    ],
                },
                {
                    "name": "technical_documents",
                    "metadata": {
                        "description": "Technical documentation",
                        "department": "Engineering",
                        "security_level": "medium",
                        "created_by": "tech_lead",
                        "version": "3.0",
                    },
                    "documents": [
                        "System architecture overview",
                        "API documentation v2.0",
                        "Database schema design",
                        "Security protocols 2024",
                        "Deployment procedures",
                    ],
                    "metadatas": [
                        {"type": "architecture", "version": "1.0"},
                        {"type": "documentation", "version": "2.0"},
                        {"type": "schema", "category": "database"},
                        {"type": "security", "year": "2024"},
                        {"type": "deployment", "version": "1.5"},
                    ],
                },
            ]

            # Create collections and add documents
            print("\n=== Creating Collections and Adding Documents ===")
            create_demo_collections(db, collections_config)

            # List all collections
            print("\n=== Listing All Collections ===")
            collections = db.list_collections()
            for collection in collections:
                print("\nCollection Details:")
                print(f"Name: {collection['name']}")
                print(f"Creation Time: {collection['creation_time']}")
                print("Metadata:", collection["metadata"])

            # Demonstrate collection management
            print("\n=== Demonstrating Collection Management ===")
            demonstrate_collection_management(db)

            # Define various types of queries
            print("\n=== Executing Various Query Scenarios ===")
            collection_queries = {
                "hr_documents": [
                    "performance review",
                    "onboarding",
                    "benefits",
                    "policy updates",
                ],
                "finance_documents": [
                    "financial report",
                    "budget",
                    "investment",
                    "revenue projections",
                ],
                "technical_documents": [
                    "architecture",
                    "API",
                    "security",
                    "deployment",
                ],
            }

            # Execute queries
            query_collections(db, collection_queries)

            # Demonstrate error handling with non-existent collection
            print("\n=== Demonstrating Error Handling ===")
            try:
                db.query_collection(
                    collection_name="non_existent_collection",
                    query_texts=["test"],
                    n_results=2,
                )
            except ProcessingError as e:
                print(f"Expected error occurred: {str(e)}")

            # Small delay to ensure all operations are complete
            time.sleep(1)

        print("\n=== Database Cleanup ===")
        print("Database was automatically cleaned up by the context manager")

    except Exception as e:
        print(f"An error occurred during the demonstration: {str(e)}")


if __name__ == "__main__":
    main()
