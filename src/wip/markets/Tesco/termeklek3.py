import requests
import json
import csv
import time
from datetime import timedelta

# ----------- Állítsd be ezeket -----------

# A bemeneti fájl (egy sor = egy ID)
input_file = "csak_id_k_lista2.csv"

# A kimeneti fájl
output_file = "termekek_adata_full.csv"

start_index = 0  # innen indul újra, pl. ha megszakadt

# A Tesco API végpont
url = "https://api.tesco.com/shoppingexperience"

# A lekérdezéshez szükséges fejléc (header)
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "x-apikey": "TvOSZJHlEk0pjniDGQFAc9Q59WGAR4dA",
    "Origin": "https://bevasarlas.tesco.hu",
    "Referer": "https://bevasarlas.tesco.hu/",
    "Accept-Language": "hu-HU",
    "Region": "HU",
    "Language": "hu-HU"
}

query = ""
if True:
    query = """query GetProduct($tpnc: String, $sellersType: SellersAttribute) {
  product(tpnc: $tpnc) {
    id
    baseProductId
    gtin
    tpnb
    tpnc
    title
    description
    brandName
    defaultImageUrl
    superDepartmentName
    departmentName
    aisleName
    seller {
      id
      __typename
    }
    shelfName
    displayType
    shelfId
    averageWeight
    isNew
    media {
      defaultImage {
        url
      }
    }
    icons {
      id
      caption
      __typename
    }
    status
    isForSale
    price {
      actual
      unitPrice
      unitOfMeasure
      __typename
    }
    promotions {
      id
      promotionType
      startDate
      endDate
      description
      unitSellingInfo
      price {
        beforeDiscount
        afterDiscount
        __typename
      }
      attributes
      qualities
      info {
        title
        __typename
      }
      __typename
    }
    productType
    sellers(type: $sellersType) {
      ...Sellers
      __typename
    }
    restrictions {
      type
      isViolated
      message
      __typename
    }
    catchWeightList {
      price
      weight
      default
      __typename
    }
    multiPackDetails {
      ...Multipack
      __typename
    }
    details {
      ...Details
      components {
        ... on CompetitorsInfo {
          competitors {
            id
            priceMatch {
              isMatching
              __typename
            }
            __typename
          }
          __typename
        }
        ... on AdditionalInfo {
          isLowEverydayPricing
          isLowPricePromise
          __typename
        }
        __typename
      }
    }
  }
}

fragment Alcohol on AlcoholInfoItemType {
  grapeVariety
  regionalInformation
  regionOfOrigin
  alcoholType
  wineColour
  percentageAlcohol
  country
  tasteCategory
  __typename
}

fragment Multipack on MultipackDetailType {
  name
  description
  sequence
  features
  boxContents
  storage
  nutritionIconInfo
  otherInformation
  ingredients
  originInformation {
    title
    value
    __typename
  }
  allergenInfo: allergens {
    name
    values
    __typename
  }
  nutritionInfo {
    name
    perComp: value1
    perServing: value2
    referenceIntake: value3
    referencePercentage: value4
    __typename
  }
  __typename
}

fragment Details on ProductDetailsType {
  ingredients
  packSize {
    value
    units
    __typename
  }
  allergenInfo: allergens {
    name
    values
    __typename
  }
  otherInformation
  additives
  netContents
  drainedWeight
  lowerAgeLimit
  recyclingInfo
  alcoholInfo: alcohol {
    ...Alcohol
    __typename
  }
  originInformation {
    title
    value
    __typename
  }
  dosage
  directions
  features
  healthClaims
  nutritionalClaims
  __typename
}

fragment Fulfilment on ProductDeliveryType {
  cutoff
  deliveryType
  start
  end
  minDeliveryDays
  maxDeliveryDays
  charges {
    value
    __typename
    criteria {
      __typename
      ... on ProductDeliveryCriteria {
        deliveryType: type
        deliveryvalue: value
        __typename
      }
      ... on ProductDeliveryBasketValueCriteria {
        type
        value
        __typename
      }
    }
  }
  __typename
}

fragment Sellers on ProductSellers {
  results {
    id
    __typename
    seller {
      id
      name
      partnerName
      businessName
      __typename
    }
    price {
      actual
      unitPrice
      unitOfMeasure
    }
    promotions {
      id
      promotionType
      startDate
      endDate
      description
      unitSellingInfo
      price {
        beforeDiscount
        afterDiscount
        __typename
      }
      attributes
      qualities
      info {
        title
        __typename
      }
      metaData {
        seo {
          afterDiscountPrice
          __typename
        }
        __typename
      }
    }
    ... on MPProduct {
      bestDelivery: fulfilment(deliveryOptions: BEST) {
        ...Fulfilment
        ... on ProductReturnType {
          __typename
          daysToReturn
        }
        __typename
      }
      fulfilment {
        ...Fulfilment
        ... on ProductReturnType {
          __typename
          daysToReturn
        }
        __typename
      }
      __typename
    }
    returnDetails {
      displayName
      returnMethod
      daysToReturn
      charges {
        value
        currency
        __typename
      }
      __typename
    }
    status
    unavailabilityReasons {
      type
      subReason
      __typename
    }
    isForSale
  }
  totalCount
  __typename
}
"""

# A lekérdezéshez szükséges payload sablon
def create_payload(product_id):
    return {
        "operationName": "GetProduct",
        "variables": {
            "includeVariations": True,
            "includeFulfilment": False,
            "tpnc": product_id,
            "skipReviews": False
        },
        "extensions": {
            "mfeName": "mfe-pdp"
        },
        "query" : query
        # Az eredeti query nagyon hosszú, itt egy rövidített verzió szerepel példaként. Kicserélheted a teljesre ha szükséges.
    }

# ----------- Fő program -----------
def flatten_json(y, prefix=''):
    out = {}
    if isinstance(y, dict):
        for k, v in y.items():
            out.update(flatten_json(v, f'{prefix}{k}.'))
    elif isinstance(y, list):
        out[prefix[:-1]] = json.dumps(y, ensure_ascii=False)
    else:
        out[prefix[:-1]] = y
    return out

# Beolvassuk az összes ID-t a fájlból
with open(input_file, "r", encoding="utf-8") as f:
    product_ids = [line.strip() for line in f if line.strip()]

product_ids = product_ids[start_index:]
results = []
start_time = time.time()

for i, pid in enumerate(product_ids, start=start_index):
    try:
        response = requests.post(url, headers=headers, json=create_payload(pid))
        if response.status_code == 200:
            data = response.json()
            product = data.get("data", {}).get("product", {})
            if product:
                flat = flatten_json(product)
                results.append(flat)
        else:
            print(f"❌ {i+1} - HTTP {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"⚠️ Hiba ID: {pid} – {e}")

    elapsed = time.time() - start_time
    avg_per_item = elapsed / (i - start_index + 1)
    remaining = len(product_ids) - (i - start_index + 1)
    eta_sec = int(remaining * avg_per_item)
    eta_str = str(timedelta(seconds=eta_sec)).split('.')[0]

    print(f"✅ {i+1}/{start_index + len(product_ids)} | {round((i - start_index + 1) / len(product_ids) * 100, 1)}% | ETA: {eta_str}")

# CSV mentés: minden kulcsot egyesítünk
if results:
    all_keys = sorted(set().union(*[r.keys() for r in results]))
    with open(output_file, "w", newline="", encoding="utf-8") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=all_keys, extrasaction='ignore')
        writer.writeheader()
        for r in results:
            writer.writerow(r)