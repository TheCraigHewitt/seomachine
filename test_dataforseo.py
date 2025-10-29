#!/usr/bin/env python3
"""
Test script for DataForSEO integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add data_sources to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'data_sources'))

from modules.dataforseo import DataForSEO

def test_connection():
    """Test basic connection to DataForSEO API"""
    print("=" * 60)
    print("Testing DataForSEO Integration")
    print("=" * 60)

    # Check credentials
    login = os.getenv('DATAFORSEO_LOGIN')
    password = os.getenv('DATAFORSEO_PASSWORD')

    print(f"\nCredentials loaded:")
    print(f"  Login: {login}")
    print(f"  Password: {'*' * len(password) if password else 'NOT SET'}")

    if not login or not password:
        print("\n❌ ERROR: Missing credentials in .env file")
        return False

    try:
        # Initialize client
        print("\n1. Initializing DataForSEO client...")
        dfs = DataForSEO()
        print("   ✓ Client initialized successfully")

        # Test 1: Simple ranking check
        print("\n2. Testing ranking check for 'podcast hosting'...")
        rankings = dfs.get_rankings(
            domain="castos.com",
            keywords=["podcast hosting"]
        )

        if rankings:
            rank_data = rankings[0]
            print(f"   ✓ API request successful")
            print(f"   Keyword: {rank_data['keyword']}")
            print(f"   Position: {rank_data['position'] or 'Not in top 100'}")
            print(f"   Search Volume: {rank_data['search_volume']:,}" if rank_data['search_volume'] else "   Search Volume: N/A")
            print(f"   Ranking URL: {rank_data['url']}" if rank_data['url'] else "   Not ranking")
        else:
            print("   ⚠ No ranking data returned")

        # Test 2: Get keyword ideas
        print("\n3. Testing keyword ideas for 'podcast'...")
        ideas = dfs.get_keyword_ideas("podcast", limit=5)

        if ideas:
            print(f"   ✓ Found {len(ideas)} keyword ideas")
            print(f"   Top suggestions:")
            for i, idea in enumerate(ideas[:3], 1):
                vol = f"{idea['search_volume']:,}" if idea['search_volume'] else "N/A"
                print(f"   {i}. {idea['keyword']} (Volume: {vol})")
        else:
            print("   ⚠ No keyword ideas returned")

        # Test 3: Get related questions
        print("\n4. Testing related questions for 'podcast hosting'...")
        questions = dfs.get_questions("podcast hosting", limit=5)

        if questions:
            print(f"   ✓ Found {len(questions)} questions")
            print(f"   Top questions:")
            for i, q in enumerate(questions[:3], 1):
                vol = f"{q['search_volume']:,}" if q['search_volume'] else "N/A"
                print(f"   {i}. {q['question']} (Volume: {vol})")
        else:
            print("   ⚠ No questions returned")

        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        print("\nDataForSEO integration is working correctly.")
        print("You can now use this data source in your agents.")

        return True

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ API Error: {e}")
        print(f"   Type: {type(e).__name__}")
        import traceback
        print(f"\n{traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
