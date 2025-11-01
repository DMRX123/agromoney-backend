import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from models.market_models import MarketData, HistoricalPrice, CandleStickData

class SampleDataGenerator:
    def __init__(self):
        # मध्य प्रदेश की सभी प्रमुख फसलें
        self.crops = [
            # अनाज
            "Wheat", "Rice", "Maize", "Jowar", "Bajra",
            # दलहन
            "Gram", "Lentil", "Pigeon Pea", "Black Gram", "Green Gram", "Cowpea",
            # तिलहन
            "Soybean", "Mustard", "Groundnut", "Sunflower", "Sesame", "Linseed", "Castor",
            # सब्जियाँ
            "Tomato", "Onion", "Potato", "Garlic", "Cabbage", "Cauliflower", "Brinjal",
            "Okra", "Peas", "Carrot", "Radish", "Cucumber", "Bitter Gourd", "Bottle Gourd", "Spinach",
            # मसाले
            "Coriander", "Chilli", "Cumin", "Fenugreek", "Turmeric", "Ginger", "Coriander Seed",
            # नकदी फसलें
            "Cotton", "Sugarcane", "Tobacco", "Jute",
            # फल
            "Mango", "Banana", "Guava", "Orange", "Papaya", "Pomegranate", "Lemon",
            # अन्य
            "Honey", "Mushroom"
        ]
        
        # मध्य प्रदेश के सभी 52 जिले
        self.districts = [
            "Agar Malwa", "Alirajpur", "Anuppur", "Ashoknagar", "Balaghat", 
            "Barwani", "Betul", "Bhind", "Bhopal", "Burhanpur", 
            "Chhatarpur", "Chhindwara", "Damoh", "Datia", "Dewas", 
            "Dhar", "Dindori", "Guna", "Gwalior", "Harda", 
            "Hoshangabad", "Indore", "Jabalpur", "Jhabua", "Katni", 
            "Khandwa", "Khargone", "Mandla", "Mandsaur", "Morena", 
            "Narsinghpur", "Neemuch", "Niwari", "Panna", "Raisen", 
            "Rajgarh", "Ratlam", "Rewa", "Sagar", "Satna", 
            "Sehore", "Seoni", "Shahdol", "Shajapur", "Sheopur", 
            "Shivpuri", "Sidhi", "Singrauli", "Tikamgarh", "Ujjain", 
            "Umaria", "Vidisha"
        ]
        
        # सभी जिलों की मंडियाँ
        self.markets = {
            "Agar Malwa": ["Agar Mandi", "Nalkheda", "Badod", "Susner"],
            "Alirajpur": ["Alirajpur Mandi", "Jobat", "Sondwa", "Katthiwada"],
            "Anuppur": ["Anuppur Mandi", "Kotma", "Jaithari", "Pushparajgarh"],
            "Ashoknagar": ["Ashoknagar Mandi", "Isagarh", "Mungaoli", "Chanderi"],
            "Balaghat": ["Balaghat Mandi", "Baihar", "Waraseoni", "Katangi", "Lalbarra"],
            "Barwani": ["Barwani Mandi", "Sendhwa", "Pansemal", "Niwali", "Rajpur"],
            "Betul": ["Betul Mandi", "Bhainsdehi", "Athner", "Multai", "Shahpur"],
            "Bhind": ["Bhind Mandi", "Ater", "Gohad", "Mehgaon", "Lahar"],
            "Bhopal": ["Bhopal Mandi", "Hathaikheda", "Berasia", "Sehore Mandi", "Vidisha Mandi"],
            "Burhanpur": ["Burhanpur Mandi", "Nepanagar", "Shahpur", "Khaknar"],
            "Chhatarpur": ["Chhatarpur Mandi", "Rajnagar", "Nowgong", "Laundi", "Gaurihar"],
            "Chhindwara": ["Chhindwara Mandi", "Pandhurna", "Amarwara", "Parasia", "Jamai"],
            "Damoh": ["Damoh Mandi", "Hatta", "Patera", "Jabera", "Batiyagarh"],
            "Datia": ["Datia Mandi", "Seondha", "Bhander", "Indergarh"],
            "Dewas": ["Dewas Mandi", "Sonkatch", "Kannod", "Bagli", "Khategaon"],
            "Dhar": ["Dhar Mandi", "Badnawar", "Sardarpur", "Kukshi", "Dharampuri"],
            "Dindori": ["Dindori Mandi", "Shahpura", "Samnapur", "Mehandwani"],
            "Guna": ["Guna Mandi", "Aron", "Raghogarh", "Bamori", "Chachoda"],
            "Gwalior": ["Gwalior Mandi", "Morar", "Dabra", "Bhitarwar", "Antari"],
            "Harda": ["Harda Mandi", "Timarni", "Khirkiya", "Rehatgaon"],
            "Hoshangabad": ["Hoshangabad Mandi", "Itarsi", "Seoni-Malwa", "Sohagpur", "Pipariya"],
            "Indore": ["Indore Mandi", "Sitapur Mandi", "Sanwer", "Mhow", "Depalpur"],
            "Jabalpur": ["Jabalpur Mandi", "Adhartal", "Khamaria", "Sihora", "Patan"],
            "Jhabua": ["Jhabua Mandi", "Petlawad", "Thandla", "Ranapur", "Meghnagar"],
            "Katni": ["Katni Mandi", "Vijayraghavgarh", "Rithi", "Badwara", "Bahoriband"],
            "Khandwa": ["Khandwa Mandi", "Harsud", "Punasa", "Pandhana"],
            "Khargone": ["Khargone Mandi", "Sanawad", "Bhikangaon", "Gogaon", "Barwah"],
            "Mandla": ["Mandla Mandi", "Nainpur", "Niwas", "Mawai", "Bichhiya"],
            "Mandsaur": ["Mandsaur Mandi", "Neemuch", "Manasa", "Sitamau", "Bhanpura"],
            "Morena": ["Morena Mandi", "Sabalgarh", "Joura", "Ambah", "Porsa"],
            "Narsinghpur": ["Narsinghpur Mandi", "Gadarwara", "Kareli", "Gotegaon", "Tendukheda"],
            "Neemuch": ["Neemuch Mandi", "Manasa", "Jawad", "Ratangarh"],
            "Niwari": ["Niwari Mandi", "Prithvipur", "Orchha", "Jatara"],
            "Panna": ["Panna Mandi", "Ajaygarh", "Gunnor", "Shahnagar", "Pawai"],
            "Raisen": ["Raisen Mandi", "Gairatganj", "Silwani", "Udaipura", "Bareli"],
            "Rajgarh": ["Rajgarh Mandi", "Biaora", "Sarangpur", "Khilchipur", "Narsinghgarh"],
            "Ratlam": ["Ratlam Mandi", "Jaora", "Alot", "Sailana", "Bajna"],
            "Rewa": ["Rewa Mandi", "Mauganj", "Hanumana", "Mangawan", "Sirmour"],
            "Sagar": ["Sagar Mandi", "Rahatgarh", "Bina", "Khurai", "Rehli"],
            "Satna": ["Satna Mandi", "Maihar", "Nagod", "Rampur-Baghelan", "Amarpatan"],
            "Sehore": ["Sehore Mandi", "Ashta", "Ichhawar", "Nasrullaganj", "Budni"],
            "Seoni": ["Seoni Mandi", "Lakhnadon", "Ghansore", "Keolari", "Barghat"],
            "Shahdol": ["Shahdol Mandi", "Burhar", "Sohagpur", "Jaisinghnagar", "Beohari"],
            "Shajapur": ["Shajapur Mandi", "Agar", "Susner", "Shujalpur", "Kalapipal"],
            "Sheopur": ["Sheopur Mandi", "Vijaypur", "Karahal", "Badoda"],
            "Shivpuri": ["Shivpuri Mandi", "Pichhore", "Karera", "Kolaras", "Narwar"],
            "Sidhi": ["Sidhi Mandi", "Waidhan", "Churhat", "Rampur-Naikin", "Gopad-Banas"],
            "Singrauli": ["Singrauli Mandi", "Waidhan", "Deosar", "Chitrangi"],
            "Tikamgarh": ["Tikamgarh Mandi", "Jatara", "Palera", "Niwari", "Prithvipur"],
            "Ujjain": ["Ujjain Mandi", "Nagda", "Khachrod", "Mahidpur", "Tarana"],
            "Umaria": ["Umaria Mandi", "Pali", "Nowrozabad", "Bandhogarh"],
            "Vidisha": ["Vidisha Mandi", "Basoda", "Kurwai", "Sironj", "Gyaraspur"]
        }
        
        # फसलों के आधार मूल्य (₹ प्रति क्विंटल) - Updated realistic prices
        self.base_prices = {
            # अनाज
            "Wheat": 2400, "Rice": 3000, "Maize": 2200, "Jowar": 2600, "Bajra": 2400,
            # दलहन
            "Gram": 5200, "Lentil": 6000, "Pigeon Pea": 7000, "Black Gram": 6500, 
            "Green Gram": 7000, "Cowpea": 4800,
            # तिलहन
            "Soybean": 4800, "Mustard": 5200, "Groundnut": 6000, "Sunflower": 5200, 
            "Sesame": 8000, "Linseed": 4800, "Castor": 5800,
            # सब्जियाँ
            "Tomato": 1500, "Onion": 2000, "Potato": 1800, "Garlic": 4500, 
            "Cabbage": 1200, "Cauliflower": 1500, "Brinjal": 2000, "Okra": 3000, 
            "Peas": 3500, "Carrot": 2200, "Radish": 1500, "Cucumber": 1800, 
            "Bitter Gourd": 2500, "Bottle Gourd": 1600, "Spinach": 1200,
            # मसाले
            "Coriander": 6500, "Chilli": 5500, "Cumin": 10000, "Fenugreek": 5000, 
            "Turmeric": 7500, "Ginger": 6500, "Coriander Seed": 7500,
            # नकदी फसलें
            "Cotton": 7000, "Sugarcane": 3500, "Tobacco": 10000, "Jute": 4200,
            # फल
            "Mango": 4500, "Banana": 2200, "Guava": 3000, "Orange": 3500, 
            "Papaya": 1800, "Pomegranate": 5500, "Lemon": 3000,
            # अन्य
            "Honey": 12000, "Mushroom": 15000
        }
        
        # फसल वोलैटिलिटी (उतार-चढ़ाव)
        self.crop_volatility = {
            "Wheat": 0.08, "Rice": 0.07, "Maize": 0.09, "Jowar": 0.08, "Bajra": 0.09,
            "Gram": 0.12, "Lentil": 0.15, "Pigeon Pea": 0.13, "Black Gram": 0.14, 
            "Green Gram": 0.12, "Cowpea": 0.11,
            "Soybean": 0.10, "Mustard": 0.11, "Groundnut": 0.12, "Sunflower": 0.10,
            "Sesame": 0.15, "Linseed": 0.13, "Castor": 0.12,
            "Tomato": 0.40, "Onion": 0.35, "Potato": 0.25, "Garlic": 0.20,
            "Cabbage": 0.18, "Cauliflower": 0.20, "Brinjal": 0.22, "Okra": 0.25,
            "Peas": 0.20, "Carrot": 0.18, "Radish": 0.15, "Cucumber": 0.22,
            "Bitter Gourd": 0.25, "Bottle Gourd": 0.20, "Spinach": 0.30,
            "Coriander": 0.20, "Chilli": 0.22, "Cumin": 0.18, "Fenugreek": 0.15,
            "Turmeric": 0.16, "Ginger": 0.20, "Coriander Seed": 0.18,
            "Cotton": 0.09, "Sugarcane": 0.06, "Tobacco": 0.12, "Jute": 0.08,
            "Mango": 0.15, "Banana": 0.12, "Guava": 0.14, "Orange": 0.16,
            "Papaya": 0.18, "Pomegranate": 0.20, "Lemon": 0.15,
            "Honey": 0.10, "Mushroom": 0.25
        }
        
        # फसल श्रेणियाँ
        self.crop_categories = {
            "Cereals": ["Wheat", "Rice", "Maize", "Jowar", "Bajra"],
            "Pulses": ["Gram", "Lentil", "Pigeon Pea", "Black Gram", "Green Gram", "Cowpea"],
            "Oilseeds": ["Soybean", "Mustard", "Groundnut", "Sunflower", "Sesame", "Linseed", "Castor"],
            "Vegetables": ["Tomato", "Onion", "Potato", "Garlic", "Cabbage", "Cauliflower", "Brinjal", 
                          "Okra", "Peas", "Carrot", "Radish", "Cucumber", "Bitter Gourd", "Bottle Gourd", "Spinach"],
            "Spices": ["Coriander", "Chilli", "Cumin", "Fenugreek", "Turmeric", "Ginger", "Coriander Seed"],
            "Cash Crops": ["Cotton", "Sugarcane", "Tobacco", "Jute"],
            "Fruits": ["Mango", "Banana", "Guava", "Orange", "Papaya", "Pomegranate", "Lemon"],
            "Other": ["Honey", "Mushroom"]
        }
    
    def get_crop_category(self, crop: str) -> str:
        """फसल की श्रेणी प्राप्त करें"""
        for category, crops in self.crop_categories.items():
            if crop in crops:
                return category
        return "Other"
    
    def generate_market_data(self, days: int = 30, crops: Optional[List[str]] = None, 
                           districts: Optional[List[str]] = None, limit: int = 1000) -> List[Dict[str, Any]]:
        """बाजार डेटा जनरेट करें"""
        data = []
        current_date = datetime.now()
        
        # Use specified crops/districts or all
        target_crops = crops if crops else self.crops
        target_districts = districts if districts else self.districts
        
        for i in range(min(days, 30)):  # Max 30 days to prevent too much data
            date = current_date - timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            for district in target_districts[:10]:  # Limit districts
                district_markets = self.markets.get(district, [f"{district} Mandi"])
                
                for crop in target_crops[:15]:  # Limit crops
                    if crop not in self.base_prices:
                        continue
                        
                    base_price = self.base_prices[crop]
                    volatility = self.crop_volatility.get(crop, 0.1)
                    
                    for market in district_markets[:2]:  # Limit markets per district
                        # मौसमी भिन्नता जोड़ें
                        seasonal_variation = self._get_seasonal_variation(crop, date.month)
                        
                        # यादृच्छिक भिन्नता
                        random_variation = random.uniform(-volatility, volatility)
                        
                        current_price = base_price * (1 + seasonal_variation) * (1 + random_variation)
                        
                        # Ensure realistic min/max prices
                        price_range = volatility * 0.6
                        min_price = current_price * (1 - price_range)
                        max_price = current_price * (1 + price_range)
                        
                        market_data = MarketData(
                            commodity=crop,
                            district=district,
                            market=market,
                            min_price=round(min_price, 2),
                            max_price=round(max_price, 2),
                            modal_price=round(current_price, 2),
                            arrival_date=date_str,
                            category=self.get_crop_category(crop)
                        )
                        data.append(market_data.to_dict())
                        
                        if len(data) >= limit:
                            return data
        
        return data
    
    def _get_seasonal_variation(self, crop: str, month: int) -> float:
        """मौसम के आधार पर मूल्य भिन्नता"""
        # रबी फसलें (बुआई: अक्टूबर-नवंबर, कटाई: मार्च-अप्रैल)
        if crop in ["Wheat", "Gram", "Mustard", "Barley"]:
            if month in [3, 4, 5]:  # कटाई का मौसम - कम मूल्य
                return random.uniform(-0.2, -0.1)
            elif month in [10, 11, 12]:  # बुआई का मौसम - उच्च मूल्य
                return random.uniform(0.1, 0.2)
            else:
                return random.uniform(-0.05, 0.05)
                
        # खरीफ फसलें (बुआई: जून-जुलाई, कटाई: सितंबर-अक्टूबर)
        elif crop in ["Rice", "Soybean", "Maize", "Cotton"]:
            if month in [9, 10, 11]:  # कटाई का मौसम - कम मूल्य
                return random.uniform(-0.25, -0.1)
            elif month in [6, 7, 8]:  # बढ़वार का मौसम - उच्च मूल्य
                return random.uniform(0.05, 0.15)
            else:
                return random.uniform(-0.05, 0.05)
                
        # सब्जियाँ - अधिक उतार-चढ़ाव
        elif crop in ["Tomato", "Onion", "Potato"]:
            return random.uniform(-0.3, 0.4)
            
        # फल - मौसमी भिन्नता
        elif crop == "Mango" and month in [4, 5, 6]:  # आम का मौसम
            return random.uniform(-0.2, 0.1)
        elif crop == "Orange" and month in [12, 1, 2]:  # संतरा का मौसम
            return random.uniform(-0.15, 0.05)
            
        else:
            # अन्य फसलें - मध्यम उतार-चढ़ाव
            return random.uniform(-0.1, 0.1)
    
    def generate_historical_data(self, crop: str, years: int = 6, 
                               district: Optional[str] = None, 
                               data_points: int = 60) -> List[Dict[str, Any]]:
        """ऐतिहासिक डेटा जनरेट करें"""
        if crop not in self.base_prices:
            return []
            
        historical_data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
        
        base_price = self.base_prices[crop]
        volatility = self.crop_volatility.get(crop, 0.1)
        
        # Use specified district or random districts
        target_districts = [district] if district else random.sample(self.districts, 5)
        
        # Calculate interval between data points
        total_days = (end_date - start_date).days
        interval_days = max(1, total_days // data_points)
        
        current_date = start_date
        points_generated = 0
        
        while current_date <= end_date and points_generated < data_points:
            # मौसमी भिन्नता
            seasonal_variation = self._get_seasonal_variation(crop, current_date.month)
            
            # दीर्घकालिक प्रवृत्ति (मुद्रास्फीति + बाजार कारक)
            years_passed = (current_date - start_date).days / 365
            trend_factor = 1.0 + (0.05 * years_passed)  # 5% वार्षिक वृद्धि
            
            # यादृच्छिक बाजार उतार-चढ़ाव
            random_factor = random.uniform(1 - volatility, 1 + volatility)
            
            price = base_price * (1 + seasonal_variation) * trend_factor * random_factor
            
            historical_price = HistoricalPrice(
                date=current_date.strftime('%Y-%m-%d'),
                price=round(price, 2),
                volume=random.randint(100, 1000),
                commodity=crop,
                district=random.choice(target_districts),
                category=self.get_crop_category(crop)
            )
            historical_data.append(historical_price.to_dict())
            
            # अगले डेटा पॉइंट के लिए आगे बढ़ें
            current_date += timedelta(days=interval_days)
            points_generated += 1
        
        return historical_data
    
    def generate_candle_data(self, crop: str, district: str, years: float = 1.0,
                           interval_days: int = 1) -> List[Dict[str, Any]]:
        """कैंडलस्टिक चार्ट के लिए OHLC डेटा जनरेट करें"""
        if crop not in self.base_prices:
            return []
            
        candle_data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=years * 365)
        
        base_price = self.base_prices[crop]
        volatility = self.crop_volatility.get(crop, 0.1)
        
        current_date = start_date
        max_points = 1000  # Safety limit
        
        while current_date <= end_date and len(candle_data) < max_points:
            # Calculate OHLC prices
            price_data = self._calculate_ohlc_price(base_price, current_date, start_date, crop, volatility)
            
            candle_stick = CandleStickData(
                date=current_date.strftime('%Y-%m-%d'),
                open_price=price_data['open'],
                high_price=price_data['high'],
                low_price=price_data['low'],
                close_price=price_data['close'],
                volume=random.randint(50, 5000),
                commodity=crop,
                district=district
            )
            candle_data.append(candle_stick.to_dict())
            
            # Move to next interval
            current_date += timedelta(days=interval_days)
        
        return candle_data
    
    def _calculate_ohlc_price(self, base_price: float, current_date: datetime, 
                            start_date: datetime, crop: str, volatility: float) -> Dict[str, float]:
        """OHLC मूल्यों की गणना करें"""
        month = current_date.month
        
        # मौसमी भिन्नता
        seasonal_factor = 1.0 + self._get_seasonal_variation(crop, month)
        
        # दीर्घकालिक प्रवृत्ति
        years_passed = (current_date - start_date).days / 365
        trend_factor = 1.0 + (0.06 * years_passed)
        
        # आधार मूल्य गणना
        base_value = base_price * seasonal_factor * trend_factor
        
        # OHLC मूल्य जनरेट करें
        open_price = base_value * random.uniform(0.95, 1.05)
        daily_change = random.uniform(-volatility, volatility)
        close_price = open_price * (1 + daily_change)
        
        # Intraday उतार-चढ़ाव
        intraday_volatility = volatility * 0.5
        high_price = max(open_price, close_price) * (1 + random.uniform(0, intraday_volatility))
        low_price = min(open_price, close_price) * (1 - random.uniform(0, intraday_volatility))
        
        # तार्किक OHLC संबंध सुनिश्चित करें
        high_price = max(open_price, close_price, high_price)
        low_price = min(open_price, close_price, low_price)
        
        return {
            'open': round(open_price, 2),
            'high': round(high_price, 2),
            'low': round(low_price, 2),
            'close': round(close_price, 2)
        }
    
    def get_crops_by_category(self, category: str) -> List[str]:
        """श्रेणी के आधार पर फसलें प्राप्त करें"""
        return self.crop_categories.get(category, [])
    
    def get_all_categories(self) -> List[str]:
        """सभी श्रेणियाँ प्राप्त करें"""
        return list(self.crop_categories.keys())
    
    def get_districts_by_region(self, region: str) -> List[str]:
        """क्षेत्र के आधार पर जिले प्राप्त करें"""
        regions = {
            "Malwa": ["Indore", "Ujjain", "Dewas", "Shajapur", "Ratlam", "Mandsaur", 
                     "Neemuch", "Agar Malwa", "Rajgarh"],
            "Nimar": ["Khandwa", "Khargone", "Barwani", "Burhanpur"],
            "Baghelkhand": ["Rewa", "Satna", "Sidhi", "Singrauli", "Umaria", "Shahdol", "Anuppur"],
            "Mahakoshal": ["Jabalpur", "Narsinghpur", "Mandla", "Dindori", "Balaghat", "Seoni", "Katni"],
            "Gird": ["Gwalior", "Bhind", "Morena", "Sheopur", "Datia"],
            "Bundelkhand": ["Sagar", "Damoh", "Chhatarpur", "Tikamgarh", "Panna", "Niwari", "Ashoknagar"],
            "Central": ["Bhopal", "Raisen", "Sehore", "Vidisha", "Hoshangabad", "Harda", "Betul", "Chhindwara"]
        }
        return regions.get(region, [])
    
    def get_random_crop_price(self, crop: str) -> Dict[str, float]:
        """फसल का यादृच्छिक मूल्य डेटा प्राप्त करें"""
        if crop not in self.base_prices:
            return {}
            
        base_price = self.base_prices[crop]
        volatility = self.crop_volatility.get(crop, 0.1)
        
        variation = random.uniform(-volatility, volatility)
        current_price = base_price * (1 + variation)
        
        return {
            'min_price': round(current_price * 0.9, 2),
            'max_price': round(current_price * 1.1, 2),
            'modal_price': round(current_price, 2)
        }