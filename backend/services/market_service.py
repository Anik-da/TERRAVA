from typing import List, Dict, Any

class MarketService:
    def __init__(self):
        # Base prices in INR per Quintal (100 kg)
        self.crop_indices = {
            "rice": {
                "crop": "Rice",
                "grade": "Basmati Grade A",
                "current_price": 3420,
                "historical_trend": [3280, 3310, 3350, 3390, 3420],
                "forecast_price": 3600,
                "demand": "High"
            },
            "wheat": {
                "crop": "Wheat",
                "grade": "Rabi Lokwan",
                "current_price": 2400,
                "historical_trend": [2320, 2350, 2380, 2390, 2400],
                "forecast_price": 2450,
                "demand": "Stable"
            },
            "tomato": {
                "crop": "Tomato",
                "grade": "Hybrid F1",
                "current_price": 1240,
                "historical_trend": [1400, 1350, 1310, 1270, 1240],
                "forecast_price": 1150,
                "demand": "Low"
            },
            "cotton": {
                "crop": "Cotton",
                "grade": "Long Staple",
                "current_price": 6800,
                "historical_trend": [6500, 6620, 6710, 6770, 6800],
                "forecast_price": 7100,
                "demand": "High"
            },
            "sustainable coffee": {
                "crop": "Sustainable Coffee",
                "grade": "Arabica Parchment",
                "current_price": 14200,
                "historical_trend": [13500, 13700, 13950, 14100, 14200],
                "forecast_price": 15000,
                "demand": "High"
            }
        }

    def get_prices(self) -> Dict[str, Any]:
        return self.crop_indices

    def calculate_forecast(self, crop: str, farm_size: float, yield_multiplier: float = 1.0) -> dict:
        crop_clean = crop.strip().lower()
        if crop_clean not in self.crop_indices:
            # Fallback values
            base_price = 2000
            forecast = 2100
            trend = [1900, 1950, 2000]
            demand = "Stable"
        else:
            meta = self.crop_indices[crop_clean]
            base_price = meta["current_price"]
            forecast = meta["forecast_price"]
            trend = meta["historical_trend"]
            demand = meta["demand"]

        # General yield estimations: hectares * average quintals per hectare
        # E.g., Coffee yields ~10 quintals/ha, Rice yields ~40 quintals/ha
        yield_per_ha = 40.0
        if "coffee" in crop_clean:
            yield_per_ha = 12.0
        elif "tomato" in crop_clean:
            yield_per_ha = 150.0
        elif "cotton" in crop_clean:
            yield_per_ha = 20.0

        estimated_yield_q = farm_size * yield_per_ha * yield_multiplier
        estimated_revenue = estimated_yield_q * base_price
        projected_revenue = estimated_yield_q * forecast
        
        # Assume 40% input production cost
        input_cost = estimated_revenue * 0.40
        estimated_profit = estimated_revenue - input_cost
        projected_profit = projected_revenue - input_cost

        return {
            "crop": crop,
            "farm_size_hectares": farm_size,
            "estimated_yield_quintals": round(estimated_yield_q, 2),
            "current_market_price_inr": base_price,
            "forecasted_market_price_inr": forecast,
            "estimated_revenue_inr": round(estimated_revenue, 2),
            "estimated_profit_inr": round(estimated_profit, 2),
            "projected_profit_inr": round(projected_profit, 2),
            "historical_trend": trend,
            "market_demand": demand
        }


market_service = MarketService()
