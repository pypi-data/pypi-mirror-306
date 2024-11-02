from flask import Flask, jsonify

class CurrencyAPI:
    def __init__(self):
        self.app = Flask(__name__)
        self.currency_dict = self.load_currency_data()

    def load_currency_data(self):
        # Hardcoded currency data
        return [
            {
                "Country": "Albania",
                "Symbol": "Lek",
                "Code": "ALL",
                "rate": 90.396622
            },
            {
                "Country": "Armenia",
                "Symbol": "Դ",
                "Code": "AMD",
                "rate": 387.62
            },
            {
                "Country": "Australia",
                "Symbol": "$",
                "Code": "AUD",
                "rate": 1.522765
            },
            {
                "Country": "Austria",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Azerbaijan",
                "Symbol": "₼",
                "Code": "AZN",
                "rate": 1.7
            },
            {
                "Country": "Bahrain",
                "Symbol": ".د.ب",
                "Code": "BHD",
                "rate": 0.376988
            },
            {
                "Country": "Bangladesh",
                "Symbol": "৳",
                "Code": "BDT",
                "rate": 119.42672
            },
            {
                "Country": "Barbados",
                "Symbol": "BD$",
                "Code": "BBD",
                "rate": 2
            },
            {
                "Country": "Belarus",
                "Symbol": "Br.",
                "Code": "BYN",
                "rate": 3.270664
            },
            {
                "Country": "Belgium",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Bosnia and Herzegovina",
                "Symbol": "KM",
                "Code": "BAM",
                "rate": 1.803495
            },
            {
                "Country": "Botswana",
                "Symbol": "P",
                "Code": "BWP",
                "rate": 13.361779
            },
            {
                "Country": "Brazil",
                "Symbol": "R$",
                "Code": "BRL",
                "rate": 5.7812
            },
            {
                "Country": "Brunei",
                "Symbol": "B$",
                "Code": "BND",
                "rate": 1.321097
            },
            {
                "Country": "Bulgaria",
                "Symbol": "лв",
                "Code": "BGN",
                "rate": 1.801445
            },
            {
                "Country": "Canada",
                "Symbol": "$",
                "Code": "CAD",
                "rate": 1.392304
            },
            {
                "Country": "Cayman Islands",
                "Symbol": "CI$",
                "Code": "KYD",
                "rate": 0.832881
            },
            {
                "Country": "China",
                "Symbol": "CN¥",
                "Code": "CNY",
                "rate": 7.118
            },
            {
                "Country": "Croatia",
                "Symbol": "kn",
                "Code": "HRK",
                "rate": 6.9382
            },
            {
                "Country": "Cyprus",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Czech Republic",
                "Symbol": "Kč",
                "Code": "CZK",
                "rate": 23.316299
            },
            {
                "Country": "Denmark",
                "Symbol": "kr.",
                "Code": "DKK",
                "rate": 6.867633
            },
            {
                "Country": "Ecuador",
                "Symbol": "$",
                "Code": "USD",
                "rate": 1
            },
            {
                "Country": "Egypt",
                "Symbol": "E£",
                "Code": "EGP",
                "rate": 48.949
            },
            {
                "Country": "Estonia",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Ethiopia",
                "Symbol": "Br",
                "Code": "ETB",
                "rate": 120.8
            },
            {
                "Country": "Finland",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "France",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Georgia",
                "Symbol": "₾",
                "Code": "GEL",
                "rate": 2.745
            },
            {
                "Country": "Germany",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Ghana",
                "Symbol": "GH₵",
                "Code": "GHS",
                "rate": 16.3
            },
            {
                "Country": "Greece",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Grenada",
                "Symbol": "EC$",
                "Code": "XCD",
                "rate": 2.70255
            },
            {
                "Country": "Guam",
                "Symbol": "$",
                "Code": "USD",
                "rate": 1
            },
            {
                "Country": "Hong Kong",
                "Symbol": "HK$",
                "Code": "HKD",
                "rate": 7.775315
            },
            {
                "Country": "Hungary",
                "Symbol": "Ft",
                "Code": "HUF",
                "rate": 375.807052
            },
            {
                "Country": "Iceland",
                "Symbol": "kr",
                "Code": "ISK",
                "rate": 137.09
            },
            {
                "Country": "India",
                "Symbol": "₹",
                "Code": "INR",
                "rate": 84.086502
            },
            {
                "Country": "Indonesia",
                "Symbol": "Rp",
                "Code": "IDR",
                "rate": 15695.934359
            },
            {
                "Country": "Iran",
                "Symbol": "﷼",
                "Code": "IRR",
                "rate": 42092.5
            },
            {
                "Country": "Ireland",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Israel",
                "Symbol": "₪",
                "Code": "ILS",
                "rate": 3.74325
            },
            {
                "Country": "Italy",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Jamaica",
                "Symbol": "JA$",
                "Code": "JMD",
                "rate": 158.112319
            },
            {
                "Country": "Japan",
                "Symbol": "JP¥",
                "Code": "JPY",
                "rate": 152.17533333
            },
            {
                "Country": "Jordan",
                "Symbol": "JD",
                "Code": "JOD",
                "rate": 0.7092
            },
            {
                "Country": "Kazakhstan",
                "Symbol": "₸",
                "Code": "KZT",
                "rate": 487.966948
            },
            {
                "Country": "Kenya",
                "Symbol": "KSh",
                "Code": "KES",
                "rate": 129
            },
            {
                "Country": "Kyrgyzstan",
                "Symbol": "лв",
                "Code": "KGS",
                "rate": 85.8
            },
            {
                "Country": "Latvia",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Lebanon",
                "Symbol": "L£",
                "Code": "LBP",
                "rate": 89550.206135
            },
            {
                "Country": "Lithuania",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Luxembourg",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Macao (SAR)",
                "Symbol": "MOP$",
                "Code": "MOP",
                "rate": 8.001343
            },
            {
                "Country": "Macedonia (FYROM)",
                "Symbol": "ден",
                "Code": "MKD",
                "rate": 56.707009
            },
            {
                "Country": "Malawi",
                "Symbol": "MK",
                "Code": "MWK",
                "rate": 1736
            },
            {
                "Country": "Malaysia",
                "Symbol": "RM",
                "Code": "MYR",
                "rate": 4.37875
            },
            {
                "Country": "Maldives",
                "Symbol": "Rf",
                "Code": "MVR",
                "rate": 15.35
            },
            {
                "Country": "Malta",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Mauritius",
                "Symbol": "Rs",
                "Code": "MUR",
                "rate": 46.109999
            },
            {
                "Country": "Mexico",
                "Symbol": "MX$",
                "Code": "MXN",
                "rate": 19.996456
            },
            {
                "Country": "Monaco",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Namibia",
                "Symbol": "N$",
                "Code": "NAD",
                "rate": 17.66
            },
            {
                "Country": "Nepal",
                "Symbol": "Rs",
                "Code": "NPR",
                "rate": 134.335083
            },
            {
                "Country": "Netherlands",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "New Zealand",
                "Symbol": "$",
                "Code": "NZD",
                "rate": 1.677304
            },
            {
                "Country": "Nicaragua",
                "Symbol": "C$",
                "Code": "NIO",
                "rate": 36.815
            },
            {
                "Country": "Niger",
                "Symbol": "CFA",
                "Code": "XOF",
                "rate": 603.930054
            },
            {
                "Country": "Nigeria",
                "Symbol": "₦",
                "Code": "NGN",
                "rate": 1642.79
            },
            {
                "Country": "Northern Cyprus",
                "Symbol": "₺",
                "Code": "TRY",
                "rate": 34.2545
            },
            {
                "Country": "Norway",
                "Symbol": "kr",
                "Code": "NOK",
                "rate": 11.02048
            },
            {
                "Country": "Oman",
                "Symbol": "ريال",
                "Code": "OMR",
                "rate": 0.384998
            },
            {
                "Country": "Pakistan",
                "Symbol": "Rs",
                "Code": "PKR",
                "rate": 277.875
            },
            {
                "Country": "Palestinian Territory, Occupied",
                "Symbol": "£P",
                "Code": "PS"
            },
            {
                "Country": "Philippines",
                "Symbol": "₱",
                "Code": "PHP",
                "rate": 58.286499
            },
            {
                "Country": "Poland",
                "Symbol": "zł",
                "Code": "PLN",
                "rate": 4.008523
            },
            {
                "Country": "Portugal",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Puerto Rico",
                "Symbol": "$",
                "Code": "USD",
                "rate": 1
            },
            {
                "Country": "Qatar",
                "Symbol": "QR",
                "Code": "QAR",
                "rate": 3.641
            },
            {
                "Country": "Romania",
                "Symbol": "lei",
                "Code": "RON",
                "rate": 4.581
            },
            {
                "Country": "Russia",
                "Symbol": "₽",
                "Code": "RUB",
                "rate": 97.373251
            },
            {
                "Country": "Rwanda",
                "Symbol": "RF",
                "Code": "RWF",
                "rate": 1360
            },
            {
                "Country": "Saudi Arabia",
                "Symbol": "SR",
                "Code": "SAR",
                "rate": 3.755652
            },
            {
                "Country": "Serbia",
                "Symbol": "РСД",
                "Code": "RSD",
                "rate": 107.764
            },
            {
                "Country": "Singapore",
                "Symbol": "S$",
                "Code": "SGD",
                "rate": 1.321996
            },
            {
                "Country": "Slovakia",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Slovenia",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "South Africa",
                "Symbol": "R",
                "Code": "ZAR",
                "rate": 17.6531
            },
            {
                "Country": "South Korea",
                "Symbol": "₩",
                "Code": "KRW",
                "rate": 1376.882315
            },
            {
                "Country": "Spain",
                "Symbol": "€",
                "Code": "EUR",
                "rate": 0.920685
            },
            {
                "Country": "Sri Lanka",
                "Symbol": "Rs",
                "Code": "LKR",
                "rate": 292.611999
            },
            {
                "Country": "Sweden",
                "Symbol": "kr",
                "Code": "SEK",
                "rate": 10.681266
            },
            {
                "Country": "Switzerland",
                "Symbol": "CHF",
                "Code": "CHF",
                "rate": 0.86527
            },
            {
                "Country": "Taiwan",
                "Symbol": "NT$",
                "Code": "TWD",
                "rate": 31.942502
            },
            {
                "Country": "Tanzania",
                "Symbol": "TSh",
                "Code": "TZS",
                "rate": 2710
            },
            {
                "Country": "Thailand",
                "Symbol": "฿",
                "Code": "THB",
                "rate": 33.83
            },
            {
                "Country": "Trinidad and Tobago",
                "Symbol": "TT$",
                "Code": "TTD",
                "rate": 6.782046
            },
            {
                "Country": "Turkey",
                "Symbol": "₺",
                "Code": "TRY",
                "rate": 34.2545
            },
            {
                "Country": "Uganda",
                "Symbol": "USh",
                "Code": "UGX",
                "rate": 3658.975878
            },
            {
                "Country": "Ukraine",
                "Symbol": "₴",
                "Code": "UAH",
                "rate": 41.188164
            },
            {
                "Country": "United Arab Emirates",
                "Symbol": "د.إ",
                "Code": "AED",
                "rate": 3.673
            },
            {
                "Country": "United Kingdom",
                "Symbol": "£",
                "Code": "GBP",
                "rate": 0.777615
            },
            {
                "Country": "United States of America",
                "Symbol": "$",
                "Code": "USD",
                "rate": 1
            },
            {
                "Country": "United States Virgin Islands",
                "Symbol": "$",
                "Code": "USD",
                "rate": 1
            },
            {
                "Country": "Vietnam",
                "Symbol": "₫",
                "Code": "VND",
                "rate": 25293.333333
            },
            {
                "Country": "Zambia",
                "Symbol": "ZK",
                "Code": "ZMW",
                "rate": 26.575928
            }
        ]
    
    def get_currency_by_country(self, country):
        """Get currency details for a specific country."""
        for currency in self.currency_dict:
            if currency["Country"].lower() == country.lower():
                return {
                "Country": currency["Country"],
                "Code": currency["Code"],
                "Symbol": currency["Symbol"]
            }
        return {"error": "Country not found"}
    
    def get_countries_by_code(self, code):
        """Get country names for a specific currency code."""
        countries = [c['Country'] for c in self.currency_dict if c['Code'].lower() == code.lower()]
        if countries:
            return  {"countries": countries}  # Return all matching countries
        return {"error": "Currency code not found"}
    
    def search_currency(self, query):
        """Search currencies by country name or currency code, returning only country and code."""
        results = [
            {"Country": c['Country'], "Code": c['Code']} 
            for c in self.currency_dict 
            if query.lower() in c['Country'].lower() or query.lower() in c['Code'].lower()
        ]
        
        if results:
            return results
        return {"error": "Entered Value Not Found"}

    

    def convert_currency(self, amount, from_code, to_code):
        """Convert currency based on provided amount and codes using USD as the base."""
        # Get the rate for the 'from' currency (how much of 1 USD is in that currency)
        from_rate = next((currency['rate'] for currency in self.currency_dict if currency['Code'] == from_code), None)
        # Get the rate for the 'to' currency (how much of 1 USD is in that currency)
        to_rate = next((currency['rate'] for currency in self.currency_dict if currency['Code'] == to_code), None)
        
        if from_rate is None:
            return {"error": f"Conversion rate for {from_code} not found."}
        if to_rate is None:
            return {"error": f"Conversion rate for {to_code} not found."}
        
        # Convert the amount to USD first
        amount_in_usd = amount / from_rate
        # Convert the USD amount to the target currency
        converted_amount = amount_in_usd * to_rate
        
        return {"converted_amount": converted_amount}


    # def get_all_currencies(self):
    #     """Get all currency details."""
    #     return self.currency_dict

    def run(self, **kwargs):
        self.app.run(**kwargs)


# If you want to run the Flask app, you can still do that
if __name__ == '__main__':
    api = CurrencyAPI()
    api.run(debug=True)
