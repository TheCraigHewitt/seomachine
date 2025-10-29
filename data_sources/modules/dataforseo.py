"""
DataForSEO API Integration

Fetches SERP data, competitor rankings, keyword research, and more.
"""

import os
import base64
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

class DataForSEO:
    """DataForSEO API client"""

    def __init__(self, login: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize DataForSEO client

        Args:
            login: API login (defaults to env var)
            password: API password (defaults to env var)
        """
        self.login = login or os.getenv('DATAFORSEO_LOGIN')
        self.password = password or os.getenv('DATAFORSEO_PASSWORD')
        self.base_url = os.getenv('DATAFORSEO_BASE_URL', 'https://api.dataforseo.com')

        if not self.login or not self.password:
            raise ValueError("DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD must be set")

        # Create auth header
        cred = f"{self.login}:{self.password}"
        encoded_cred = base64.b64encode(cred.encode('ascii')).decode('ascii')
        self.headers = {
            'Authorization': f'Basic {encoded_cred}',
            'Content-Type': 'application/json'
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _post(self, endpoint: str, data: List[Dict]) -> Dict:
        """Make POST request to DataForSEO API"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()

    def get_rankings(
        self,
        domain: str,
        keywords: List[str],
        location_code: int = 2840,  # USA
        language_code: str = "en"
    ) -> List[Dict[str, Any]]:
        """
        Get ranking positions for specific keywords

        Args:
            domain: Your domain (e.g., "castos.com")
            keywords: List of keywords to check
            location_code: DataForSEO location code (2840 = USA)
            language_code: Language code

        Returns:
            List of ranking data for each keyword
        """
        tasks = []
        for keyword in keywords:
            tasks.append({
                "keyword": keyword,
                "location_code": location_code,
                "language_code": language_code,
                "device": "desktop",
                "os": "windows"
            })

        response = self._post('/v3/serp/google/organic/live/advanced', tasks)

        results = []
        if response['status_code'] == 20000:
            for task in response['tasks']:
                if task['status_code'] == 20000:
                    keyword = task['data']['keyword']
                    items = task['result'][0].get('items', [])

                    # Find domain position
                    position = None
                    url = None
                    for i, item in enumerate(items, 1):
                        if domain in item.get('domain', ''):
                            position = i
                            url = item.get('url')
                            break

                    results.append({
                        'keyword': keyword,
                        'domain': domain,
                        'position': position,
                        'url': url,
                        'ranking': position is not None,
                        'search_volume': task['result'][0].get('keyword_data', {}).get('keyword_info', {}).get('search_volume'),
                        'cpc': task['result'][0].get('keyword_data', {}).get('keyword_info', {}).get('cpc')
                    })

        return results

    def get_serp_data(
        self,
        keyword: str,
        location_code: int = 2840,
        limit: int = 100
    ) -> Dict[str, Any]:
        """
        Get complete SERP data for a keyword

        Args:
            keyword: Search keyword
            location_code: DataForSEO location code
            limit: Number of results to return

        Returns:
            Dict with SERP data including all ranking pages
        """
        data = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": "en",
            "device": "desktop",
            "os": "windows",
            "depth": limit
        }]

        response = self._post('/v3/serp/google/organic/live/advanced', data)

        if response['status_code'] != 20000:
            return {'error': 'API request failed'}

        task = response['tasks'][0]
        if task['status_code'] != 20000:
            return {'error': 'Task failed'}

        result = task['result'][0]

        # Extract organic results
        organic_results = []
        for item in result.get('items', []):
            if item['type'] == 'organic':
                organic_results.append({
                    'position': item.get('rank_absolute'),
                    'url': item.get('url'),
                    'domain': item.get('domain'),
                    'title': item.get('title'),
                    'description': item.get('description'),
                    'breadcrumb': item.get('breadcrumb')
                })

        # Extract SERP features
        features = []
        for item in result.get('items', []):
            if item['type'] != 'organic':
                features.append(item['type'])

        keyword_data = result.get('keyword_data', {}).get('keyword_info', {})

        return {
            'keyword': keyword,
            'search_volume': keyword_data.get('search_volume'),
            'cpc': keyword_data.get('cpc'),
            'competition': keyword_data.get('competition'),
            'organic_results': organic_results,
            'features': list(set(features)),
            'total_results': result.get('items_count', 0)
        }

    def analyze_competitor(
        self,
        competitor_domain: str,
        keywords: List[str],
        your_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze competitor rankings vs yours

        Args:
            competitor_domain: Competitor's domain
            keywords: Keywords to compare
            your_domain: Your domain (optional)

        Returns:
            Comparative ranking analysis
        """
        tasks = []
        for keyword in keywords:
            tasks.append({
                "keyword": keyword,
                "location_code": 2840,
                "language_code": "en",
                "device": "desktop"
            })

        response = self._post('/v3/serp/google/organic/live/advanced', tasks)

        comparison = []
        for i, task in enumerate(response['tasks']):
            if task['status_code'] == 20000:
                keyword = keywords[i]
                items = task['result'][0].get('items', [])

                competitor_pos = None
                your_pos = None

                for j, item in enumerate(items, 1):
                    domain = item.get('domain', '')
                    if competitor_domain in domain:
                        competitor_pos = j
                    if your_domain and your_domain in domain:
                        your_pos = j

                gap = None
                if competitor_pos and your_pos:
                    gap = your_pos - competitor_pos
                elif competitor_pos and not your_pos:
                    gap = "Not ranking"

                comparison.append({
                    'keyword': keyword,
                    'competitor_position': competitor_pos,
                    'your_position': your_pos,
                    'gap': gap,
                    'opportunity': 'high' if competitor_pos and not your_pos else 'medium' if gap and gap > 10 else 'low'
                })

        return {
            'competitor': competitor_domain,
            'your_domain': your_domain,
            'comparison': comparison
        }

    def get_keyword_ideas(
        self,
        seed_keyword: str,
        location_code: int = 2840,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get related keyword ideas

        Args:
            seed_keyword: Starting keyword
            location_code: Location code
            limit: Number of ideas to return

        Returns:
            List of related keywords with search volume, difficulty
        """
        data = [{
            "keyword": seed_keyword,
            "location_code": location_code,
            "language_code": "en",
            "include_serp_info": True,
            "limit": limit
        }]

        response = self._post('/v3/dataforseo_labs/google/related_keywords/live', data)

        if response['status_code'] != 20000:
            return []

        task = response['tasks'][0]
        if task['status_code'] != 20000:
            return []

        keywords = []
        for item in task['result'][0].get('items', []):
            keywords.append({
                'keyword': item.get('keyword_data', {}).get('keyword'),
                'search_volume': item.get('keyword_data', {}).get('keyword_info', {}).get('search_volume'),
                'cpc': item.get('keyword_data', {}).get('keyword_info', {}).get('cpc'),
                'competition': item.get('keyword_data', {}).get('keyword_info', {}).get('competition'),
                'avg_position': item.get('serp_info', {}).get('se_results_count')
            })

        # Sort by search volume
        keywords.sort(key=lambda x: x['search_volume'] or 0, reverse=True)

        return keywords

    def get_questions(
        self,
        keyword: str,
        location_code: int = 2840,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get question-based queries related to keyword

        Args:
            keyword: Seed keyword
            location_code: Location code
            limit: Number of questions to return

        Returns:
            List of question queries
        """
        data = [{
            "keyword": keyword,
            "location_code": location_code,
            "language_code": "en",
            "limit": limit
        }]

        response = self._post('/v3/dataforseo_labs/google/related_keywords/live', data)

        if response['status_code'] != 20000:
            return []

        task = response['tasks'][0]
        if task['status_code'] != 20000:
            return []

        questions = []
        for item in task['result'][0].get('items', []):
            kw = item.get('keyword_data', {}).get('keyword', '')

            # Filter for questions
            if any(kw.lower().startswith(q) for q in ['how', 'what', 'why', 'when', 'where', 'who', 'can', 'should', 'is', 'are', 'does']):
                questions.append({
                    'question': kw,
                    'search_volume': item.get('keyword_data', {}).get('keyword_info', {}).get('search_volume'),
                    'cpc': item.get('keyword_data', {}).get('keyword_info', {}).get('cpc')
                })

        # Sort by search volume
        questions.sort(key=lambda x: x['search_volume'] or 0, reverse=True)

        return questions

    def get_domain_metrics(
        self,
        domain: str
    ) -> Dict[str, Any]:
        """
        Get domain overview metrics

        Args:
            domain: Domain to analyze

        Returns:
            Dict with domain metrics
        """
        data = [{
            "target": domain,
            "location_code": 2840,
            "language_code": "en"
        }]

        response = self._post('/v3/dataforseo_labs/google/domain_metrics/live', data)

        if response['status_code'] != 20000:
            return {}

        task = response['tasks'][0]
        if task['status_code'] != 20000:
            return {}

        metrics = task['result'][0].get('items', [{}])[0].get('metrics', {})

        return {
            'domain': domain,
            'organic_keywords': metrics.get('organic', {}).get('count'),
            'organic_traffic': metrics.get('organic', {}).get('etv'),
            'domain_rank': metrics.get('organic', {}).get('rank'),
            'backlinks': metrics.get('backlinks', {})
        }

    def check_ranking_history(
        self,
        domain: str,
        keyword: str,
        months_back: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Get ranking history for a keyword (requires historical data)

        Args:
            domain: Your domain
            keyword: Keyword to track
            months_back: Months of history

        Returns:
            List of historical rankings
        """
        # Note: This requires DataForSEO's ranking tracking to be set up
        # This is a simplified version - actual implementation may vary

        data = [{
            "target": domain,
            "keyword": keyword,
            "location_code": 2840,
            "language_code": "en"
        }]

        try:
            response = self._post('/v3/serp/google/organic/ranking_history/live', data)

            if response['status_code'] == 20000:
                task = response['tasks'][0]
                if task['status_code'] == 20000:
                    return task['result'][0].get('items', [])
        except:
            pass

        return []


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv('data_sources/config/.env')

    dfs = DataForSEO()

    print("Checking rankings for Castos...")
    rankings = dfs.get_rankings(
        domain="castos.com",
        keywords=["podcast hosting", "podcast analytics", "private podcast"]
    )

    for rank in rankings:
        print(f"\nKeyword: {rank['keyword']}")
        print(f"Position: {rank['position'] or 'Not ranking'}")
        print(f"Search Volume: {rank['search_volume']:,}" if rank['search_volume'] else "Search Volume: N/A")

    print("\n\nGetting SERP data for 'podcast monetization'...")
    serp = dfs.get_serp_data("podcast monetization")

    print(f"Search Volume: {serp['search_volume']:,}")
    print(f"SERP Features: {', '.join(serp['features'])}")
    print(f"\nTop 10 Results:")
    for result in serp['organic_results'][:10]:
        print(f"{result['position']}. {result['domain']}")
        print(f"   {result['url']}")

    print("\n\nRelated questions for 'podcast monetization':")
    questions = dfs.get_questions("podcast monetization")
    for q in questions[:10]:
        print(f"- {q['question']}")
        print(f"  Volume: {q['search_volume']:,}" if q['search_volume'] else "  Volume: N/A")
