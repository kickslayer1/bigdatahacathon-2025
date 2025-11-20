"""
API Integration Module for External Trade Data Sources
"""

import requests
import pandas as pd
import logging
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time
from config import get_config

logger = logging.getLogger(__name__)

class TradeDataAPI:
    """Enhanced trade data API integration"""
    
    def __init__(self):
        self.config = get_config()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Rwanda-Trade-Dashboard/1.0'
        })
        
    def get_world_bank_data(self, indicator: str, countries: List[str] = None, 
                           years: str = "2015:2023") -> Optional[pd.DataFrame]:
        """
        Fetch data from World Bank API
        
        Popular indicators:
        - NE.EXP.GNFS.ZS: Exports of goods and services (% of GDP)
        - NE.IMP.GNFS.ZS: Imports of goods and services (% of GDP)
        - TX.VAL.MRCH.CD: Merchandise exports (current US$)
        - TM.VAL.MRCH.CD: Merchandise imports (current US$)
        """
        try:
            countries_str = ";".join(countries) if countries else "all"
            url = f"https://api.worldbank.org/v2/country/{countries_str}/indicator/{indicator}"
            
            params = {
                'date': years,
                'format': 'json',
                'per_page': 10000
            }
            
            logger.info(f"Fetching World Bank data: {indicator}")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if len(data) > 1 and data[1]:
                df = pd.DataFrame(data[1])
                logger.info(f"Retrieved {len(df)} records from World Bank")
                return df
            return None
            
        except Exception as e:
            logger.error(f"World Bank API error: {e}")
            return None
    
    def get_un_comtrade_data(self, reporter: str = "646", partner: str = "all", 
                            trade_flow: str = "1", years: str = "2023") -> Optional[pd.DataFrame]:
        """
        Fetch data from UN Comtrade API
        
        Args:
            reporter: Country code (646 = Rwanda)
            partner: Partner country code or "all"
            trade_flow: 1=Import, 2=Export, all=All
            years: Year or year range
        """
        try:
            # UN Comtrade has rate limits
            time.sleep(1)
            
            url = "https://comtradeapi.un.org/data/v1/get/C/A/HS"
            
            params = {
                'freq': 'A',  # Annual
                'clCode': 'TOTAL',  # All commodities
                'period': years,
                'reporterCode': reporter,
                'partnerCode': partner,
                'flowCode': trade_flow,
                'partner2Code': '',
                'customsCode': 'C00',
                'motCode': '0',
                'maxRecords': 10000,
                'format': 'json',
                'aggregateBy': 'none',
                'breakdownMode': 'classic',
                'includeDesc': True
            }
            
            logger.info(f"Fetching UN Comtrade data for Rwanda")
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and data['data']:
                df = pd.DataFrame(data['data'])
                logger.info(f"Retrieved {len(df)} records from UN Comtrade")
                return df
            return None
            
        except Exception as e:
            logger.error(f"UN Comtrade API error: {e}")
            return None
    
    def get_imf_dots_data(self, country_code: str = "646") -> Optional[Dict]:
        """
        Fetch data from IMF Direction of Trade Statistics
        Note: IMF API requires registration for full access
        """
        try:
            # This is a simplified example - full implementation would require API key
            url = f"http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/DOT/{country_code}"
            
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            logger.error(f"IMF DOTS API error: {e}")
            return None
    
    def get_wto_stats(self) -> Optional[Dict]:
        """
        Fetch data from WTO Statistics Database
        Note: WTO provides bulk download files rather than real-time API
        """
        try:
            # WTO provides downloadable datasets
            # This would typically involve downloading and parsing CSV/Excel files
            url = "https://www.wto.org/english/res_e/statis_e/daily_update_e/merchandise_trade_product.zip"
            
            # For demo purposes, return sample structure
            return {
                'message': 'WTO data requires file download and processing',
                'download_url': url,
                'suggested_approach': 'Download quarterly/annual files and import to database'
            }
            
        except Exception as e:
            logger.error(f"WTO Stats error: {e}")
            return None

class RegionalDataProvider:
    """African and regional trade data provider"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_afdb_data(self) -> Dict:
        """
        African Development Bank economic data
        """
        return {
            'source': 'African Development Bank',
            'url': 'https://dataportal.opendataforafrica.org/',
            'description': 'Comprehensive African economic and trade statistics',
            'access': 'Free with registration',
            'data_types': [
                'Regional trade flows',
                'Economic indicators',
                'Infrastructure data',
                'Agricultural trade'
            ]
        }
    
    def get_eac_data(self) -> Dict:
        """
        East African Community trade data
        """
        return {
            'source': 'East African Community',
            'url': 'https://www.eac.int/statistics',
            'description': 'EAC regional trade and integration statistics',
            'data_types': [
                'Intra-EAC trade',
                'Common external tariff data',
                'Trade facilitation metrics',
                'Regional value chains'
            ]
        }
    
    def get_afreximbank_data(self) -> Dict:
        """
        African Export-Import Bank trade data
        """
        return {
            'source': 'African Export-Import Bank',
            'url': 'https://www.afreximbank.com/african-trade-report/',
            'description': 'African Trade Report and statistics',
            'data_types': [
                'Intra-African trade',
                'Trade finance data',
                'Export credit information',
                'Regional trade agreements impact'
            ]
        }

def get_recommended_data_sources() -> Dict:
    """
    Get comprehensive list of recommended trade data sources
    """
    return {
        'primary_sources': {
            'world_bank': {
                'name': 'World Bank Open Data',
                'url': 'https://data.worldbank.org/',
                'api_url': 'https://datahelpdesk.worldbank.org/knowledgebase/articles/889392',
                'description': 'Comprehensive economic indicators including trade data',
                'cost': 'Free',
                'rate_limit': 'No strict limits',
                'data_quality': 'High',
                'update_frequency': 'Annual',
                'rwanda_specific': True,
                'sample_indicators': [
                    'NE.EXP.GNFS.ZS - Exports of goods and services (% of GDP)',
                    'TX.VAL.MRCH.CD - Merchandise exports (current US$)',
                    'TM.VAL.MRCH.CD - Merchandise imports (current US$)',
                    'BX.GSR.GNFS.CD - Exports of goods and services (BoP, current US$)'
                ]
            },
            'un_comtrade': {
                'name': 'UN Comtrade Database',
                'url': 'https://comtradeplus.un.org/',
                'api_url': 'https://comtradeapi.un.org/',
                'description': 'Most comprehensive trade statistics database globally',
                'cost': 'Free (with limits), Premium subscription available',
                'rate_limit': '100 requests/hour (free), 10,000/hour (premium)',
                'data_quality': 'Very High',
                'update_frequency': 'Monthly',
                'rwanda_specific': True,
                'commodity_detail': 'HS 6-digit level'
            },
            'imf_dots': {
                'name': 'IMF Direction of Trade Statistics',
                'url': 'https://data.imf.org/regular.aspx?key=61013712',
                'description': 'Bilateral trade flow data',
                'cost': 'Free registration required',
                'data_quality': 'High',
                'update_frequency': 'Monthly',
                'rwanda_specific': True
            }
        },
        'regional_sources': {
            'afdb': {
                'name': 'African Development Bank Data Portal',
                'url': 'https://dataportal.opendataforafrica.org/',
                'description': 'African economic and development statistics',
                'focus': 'African continent',
                'cost': 'Free with registration'
            },
            'eac_statistics': {
                'name': 'East African Community Statistics',
                'url': 'https://www.eac.int/statistics',
                'description': 'Regional trade and integration data',
                'focus': 'East African Community',
                'cost': 'Free'
            },
            'afreximbank': {
                'name': 'Afreximbank African Trade Report',
                'url': 'https://www.afreximbank.com/african-trade-report/',
                'description': 'Annual comprehensive African trade analysis',
                'focus': 'Intra-African trade',
                'cost': 'Free download'
            }
        },
        'specialized_sources': {
            'wto_stats': {
                'name': 'WTO Statistics Database',
                'url': 'https://www.wto.org/english/res_e/statis_e/statis_e.htm',
                'description': 'Global trade statistics and trends',
                'cost': 'Free',
                'format': 'Downloadable datasets'
            },
            'oecd_trade': {
                'name': 'OECD Trade Statistics',
                'url': 'https://www.oecd.org/trade/topics/trade-statistics/',
                'description': 'Trade in goods and services statistics',
                'cost': 'Free',
                'focus': 'OECD countries + key partners'
            },
            'unctad_stat': {
                'name': 'UNCTAD Statistics',
                'url': 'https://unctadstat.unctad.org/',
                'description': 'Trade, investment and development statistics',
                'cost': 'Free',
                'focus': 'Developing countries'
            }
        },
        'implementation_guide': {
            'recommended_approach': [
                '1. Start with World Bank API for general economic indicators',
                '2. Use UN Comtrade for detailed commodity trade data',
                '3. Supplement with regional sources (EAC, AfDB) for context',
                '4. Download WTO/OECD datasets for comparative analysis'
            ],
            'data_integration_strategy': [
                'Create automated ETL pipelines for regular data updates',
                'Implement data validation and quality checks',
                'Use caching to minimize API calls',
                'Set up monitoring for data source availability'
            ],
            'technical_considerations': [
                'API rate limiting and authentication',
                'Data format standardization',
                'Error handling and fallback mechanisms',
                'Data versioning and historical tracking'
            ]
        }
    }

# API client instances
trade_api = TradeDataAPI()
regional_provider = RegionalDataProvider()

def fetch_global_trade_data(country_code: str = "RW") -> Dict:
    """
    Fetch comprehensive global trade data for a country
    """
    results = {
        'country': country_code,
        'timestamp': datetime.now().isoformat(),
        'data_sources': {},
        'summary': {}
    }
    
    try:
        # World Bank data
        wb_exports = trade_api.get_world_bank_data(
            'TX.VAL.MRCH.CD',  # Merchandise exports
            countries=[country_code]
        )
        if wb_exports is not None:
            results['data_sources']['world_bank_exports'] = wb_exports.to_dict('records')
        
        # UN Comtrade data (sample)
        comtrade_data = trade_api.get_un_comtrade_data(reporter="646")  # Rwanda
        if comtrade_data is not None:
            results['data_sources']['un_comtrade'] = comtrade_data.to_dict('records')
        
        # Regional data sources
        results['regional_sources'] = {
            'afdb': regional_provider.get_afdb_data(),
            'eac': regional_provider.get_eac_data(),
            'afreximbank': regional_provider.get_afreximbank_data()
        }
        
        # Add recommendations
        results['recommended_sources'] = get_recommended_data_sources()
        
        logger.info(f"Successfully compiled trade data for {country_code}")
        
    except Exception as e:
        logger.error(f"Error fetching global trade data: {e}")
        results['error'] = str(e)
    
    return results