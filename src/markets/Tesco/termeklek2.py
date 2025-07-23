import requests
import json
import csv
import time
from datetime import timedelta

# ----------- Állítsd be ezeket -----------

# A bemeneti fájl (egy sor = egy ID)
input_file = "csak_id_k_lista3.csv"

# A kimeneti fájl
output_file = "termek_adatok3.csv"

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

# A lekérdezéshez szükséges payload sablon
def create_payload(product_id):
    return {
        "operationName": "GetProduct",
        "variables": {
            "includeVariations": True,
            "includeFulfilment": False,
            "tpnc": product_id,
            "skipReviews": False,
            "offset": 0,
            "count": 10
        },
        "extensions": {
            "mfeName": "mfe-pdp"
        },
        "query" : "query GetProduct($tpnc: String, $skipReviews: Boolean!, $offset: Int, $count: Int, $includeVariations: Boolean = false, $includeFulfilment: Boolean = false) {\n  product(tpnc: $tpnc) {\n    id\n    baseProductId\n    isRestrictedOrderAmendment\n    gtin\n    tpnb\n    tpnc\n    title\n    description\n    brandName\n    isInFavourites\n    defaultImageUrl\n    superDepartmentName\n    superDepartmentId\n    departmentName\n    departmentId\n    aisleName\n    aisleId\n    shelfName\n    displayType\n    shelfId\n    averageWeight\n    bulkBuyLimit\n    bulkBuyLimitGroupId\n    bulkBuyLimitMessage\n    groupBulkBuyLimit\n    isForSale\n    isNew\n    depositAmount\n    media {\n      defaultImage {\n        url\n        aspectRatio\n        __typename\n      }\n      __typename\n    }\n    icons {\n      id\n      caption\n      __typename\n    }\n    status\n    unavailabilityReasons {\n      type\n      subReason\n      __typename\n    }\n    productType\n    charges {\n      ... on ProductDepositReturnCharge {\n        __typename\n        amount\n      }\n      __typename\n    }\n    __typename\n    ... on FNFProduct {\n      fulfilment @include(if: $includeFulfilment) {\n        ...Fulfilment\n        ... on ProductReturnType {\n          __typename\n          daysToReturn\n        }\n        __typename\n      }\n      variations {\n        ...VariationProducts @include(if: $includeVariations)\n        __typename\n      }\n      media {\n        defaultImage {\n          url\n          aspectRatio\n          __typename\n        }\n        images {\n          url\n          aspectRatio\n          ... on ModelImage {\n            modelHeight\n            modelWearingSize\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      returnDetails {\n        displayName\n        returnMethod\n        daysToReturn\n        charges {\n          value\n          currency\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n    ... on MPProduct {\n      fulfilment @include(if: $includeFulfilment) {\n        ...Fulfilment\n        ... on ProductReturnType {\n          __typename\n          daysToReturn\n        }\n        __typename\n      }\n      variations {\n        ...VariationProducts @include(if: $includeVariations)\n        __typename\n      }\n      __typename\n    }\n    seller {\n      id\n      name\n      partnerName\n      businessName\n      __typename\n    }\n    images {\n      display {\n        default {\n          url\n          originalUrl\n          __typename\n        }\n        zoom {\n          url\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    foodIcons\n    shelfLife {\n      url\n      message\n      __typename\n    }\n    restrictions {\n      type\n      isViolated\n      message\n      __typename\n    }\n    distributorAddress {\n      ...Address\n      __typename\n    }\n    manufacturerAddress {\n      ...Address\n      __typename\n    }\n    importerAddress {\n      ...Address\n      __typename\n    }\n    returnTo {\n      ...Address\n      __typename\n    }\n    maxWeight\n    minWeight\n    catchWeightList {\n      price\n      weight\n      default\n      __typename\n    }\n    multiPackDetails {\n      ...Multipack\n      __typename\n    }\n    details {\n      energyEfficiency {\n        class\n        energyClassUrl\n        productInfoDoc\n        __typename\n      }\n      clothingInfo {\n        fibreComposition\n        specialFeature\n        careInstructions\n        sizeChart {\n          url\n          id\n          __typename\n        }\n        __typename\n      }\n      ...Details\n      components {\n        ... on CompetitorsInfo {\n          competitors {\n            id\n            priceMatch {\n              isMatching\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        ... on AdditionalInfo {\n          isLowEverydayPricing\n          isLowPricePromise\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    price {\n      actual\n      unitPrice\n      unitOfMeasure\n      __typename\n    }\n    promotions {\n      id\n      promotionType\n      startDate\n      endDate\n      description\n      unitSellingInfo\n      price {\n        beforeDiscount\n        afterDiscount\n        __typename\n      }\n      attributes\n      qualities\n      info {\n        title\n        __typename\n      }\n      __typename\n    }\n    reviews(offset: $offset, count: $count) @skip(if: $skipReviews) {\n      info {\n        offset\n        total\n        page\n        count\n        __typename\n      }\n      entries {\n        rating {\n          value\n          range\n          __typename\n        }\n        author {\n          nickname\n          authoredByMe\n          __typename\n        }\n        status\n        summary\n        text\n        syndicated\n        syndicationSource {\n          name\n          clientUrl\n          __typename\n        }\n        submissionDateTime\n        reviewId\n        verifiedBuyer\n        promotionalReview\n        __typename\n      }\n      stats {\n        noOfReviews\n        overallRating\n        __typename\n      }\n      __typename\n    }\n  }\n}\n\nfragment GDA on GuidelineDailyAmountType {\n  title\n  dailyAmounts {\n    name\n    value\n    percent\n    rating\n    __typename\n  }\n  __typename\n}\n\nfragment Alcohol on AlcoholInfoItemType {\n  tastingNotes\n  grapeVariety\n  vinificationDetails\n  history\n  regionalInformation\n  storageType\n  storageInstructions\n  alcoholUnitsOtherText\n  regionOfOrigin\n  alcoholType\n  wineColour\n  alcoholUnits\n  percentageAlcohol\n  currentVintage\n  producer\n  typeOfClosure\n  wineMaker\n  packQty\n  packMeasure\n  country\n  tasteCategory\n  alcoholByVolumeOtherText\n  wineEffervescence\n  legalNotice {\n    message\n    link\n    __typename\n  }\n  __typename\n}\n\nfragment Nutrition on NutritionalInfoItemType {\n  name\n  perComp: value1\n  perServing: value2\n  referenceIntake: value3\n  referencePercentage: value4\n  __typename\n}\n\nfragment CookingInstructions on CookingInstructionsType {\n  oven {\n    chilled {\n      time\n      instructions\n      temperature {\n        value\n        __typename\n      }\n      __typename\n    }\n    frozen {\n      time\n      instructions\n      temperature {\n        value\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  microwave {\n    chilled {\n      detail {\n        step\n        T650\n        T750\n        T850\n        __typename\n      }\n      instructions\n      __typename\n    }\n    frozen {\n      detail {\n        step\n        T650\n        T750\n        T850\n        __typename\n      }\n      instructions\n      __typename\n    }\n    __typename\n  }\n  cookingMethods {\n    name\n    instructions\n    time\n    __typename\n  }\n  otherInstructions\n  cookingGuidelines\n  cookingPrecautions\n  __typename\n}\n\nfragment Address on AddressType {\n  addressLine1\n  addressLine2\n  addressLine3\n  addressLine4\n  addressLine5\n  addressLine6\n  addressLine7\n  addressLine8\n  addressLine9\n  addressLine10\n  addressLine11\n  addressLine12\n  addressLine13\n  addressLine14\n  addressLine15\n  addressLine16\n  addressLine18\n  addressLine19\n  addressLine20\n  __typename\n}\n\nfragment Multipack on MultipackDetailType {\n  name\n  description\n  sequence\n  numberOfUses\n  features\n  boxContents\n  storage\n  nutritionIconInfo\n  nutritionalClaims\n  healthClaims\n  preparationAndUsage\n  otherInformation\n  ingredients\n  cookingInstructions {\n    ...CookingInstructions\n    __typename\n  }\n  originInformation {\n    title\n    value\n    __typename\n  }\n  guidelineDailyAmount {\n    ...GDA\n    __typename\n  }\n  allergenInfo: allergens {\n    name\n    values\n    __typename\n  }\n  nutritionInfo {\n    name\n    perComp: value1\n    perServing: value2\n    referenceIntake: value3\n    referencePercentage: value4\n    __typename\n  }\n  __typename\n}\n\nfragment Details on ProductDetailsType {\n  ingredients\n  legalLabelling\n  packSize {\n    value\n    units\n    __typename\n  }\n  allergenInfo: allergens {\n    name\n    values\n    __typename\n  }\n  marketingTextInfo: marketing\n  storage\n  nutritionInfo: nutrition {\n    ...Nutrition\n    __typename\n  }\n  specifications {\n    specificationAttributes {\n      attributeName: name\n      attributeValue: value\n      __typename\n    }\n    __typename\n  }\n  otherNutritionInformation\n  hazardInfo {\n    chemicalName\n    productName\n    signalWord\n    statements\n    symbolCodes\n    __typename\n  }\n  guidelineDailyAmount {\n    ...GDA\n    __typename\n  }\n  numberOfUses\n  preparationAndUsage\n  freezingInstructions {\n    standardGuidelines\n    freezingGuidelines\n    defrosting\n    __typename\n  }\n  manufacturerMarketing\n  productMarketing\n  brandMarketing\n  otherInformation\n  additives\n  warnings\n  netContents\n  drainedWeight\n  safetyWarning\n  lowerAgeLimit\n  upperAgeLimit\n  healthmark\n  recyclingInfo\n  nappyInfo: nappies {\n    quantity\n    nappySize\n    __typename\n  }\n  alcoholInfo: alcohol {\n    ...Alcohol\n    __typename\n  }\n  cookingInstructions {\n    ...CookingInstructions\n    __typename\n  }\n  originInformation {\n    title\n    value\n    __typename\n  }\n  dosage\n  preparationGuidelines\n  directions\n  features\n  healthClaims\n  boxContents\n  nutritionalClaims\n  __typename\n}\n\nfragment VariationProducts on VariationsType {\n  products {\n    title\n    tpnc\n    tpnb\n    id\n    variationAttributes {\n      ...VariationAttributes\n      __typename\n    }\n    isForSale\n    gtin\n    status\n    promotions {\n      id\n      description\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment VariationAttributes on VariationAttributesType {\n  attributeGroup\n  attributeGroupData {\n    name\n    value\n    attributes {\n      name\n      value\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment Fulfilment on ProductDeliveryType {\n  cutoff\n  deliveryType\n  start\n  end\n  minDeliveryDays\n  maxDeliveryDays\n  charges {\n    value\n    __typename\n    criteria {\n      __typename\n      ... on ProductDeliveryCriteria {\n        deliveryType: type\n        deliveryvalue: value\n        __typename\n      }\n      ... on ProductDeliveryBasketValueCriteria {\n        type\n        value\n        __typename\n      }\n    }\n  }\n  __typename\n}\n"
        # Az eredeti query nagyon hosszú, itt egy rövidített verzió szerepel példaként. Kicserélheted a teljesre ha szükséges.
    }

# ----------- Fő program -----------

# Beolvassuk az összes ID-t a fájlból
with open(input_file, "r", encoding="utf-8") as f:
    product_ids = [line.strip() for line in f if line.strip()]

with open(input_file, "r", encoding="utf-8") as f:
    product_ids = [line.strip() for line in f if line.strip()]

product_ids = product_ids[start_index:]
total = len(product_ids)

first_row = start_index == 0
start_time = time.time()

with open(output_file, "a" if not first_row else "w", newline="", encoding="utf-8") as f_out:
    writer = None

    for i, pid in enumerate(product_ids, start=start_index):
        iter_start = time.time()
        payload = create_payload(pid)
        try:
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                data = response.json()
                print(data)
                product = data.get("data", {}).get("product", {})
                if product:
                    price_data = product.get("price", {})
                    details = product.get("details", {})

                    result = {
                        "id": product.get("id"),
                        "gtin": product.get("gtin"),
                        "title": product.get("title"),
                        "description": " ".join(product.get("description", [])) if isinstance(product.get("description"), list) else product.get("description"),
                        "brandName": product.get("brandName"),
                        "defaultImageUrl": product.get("defaultImageUrl"),
                        "superDepartmentName": product.get("superDepartmentName"),
                        "departmentName": product.get("departmentName"),
                        "aisleName": product.get("aisleName"),
                        "shelfName": product.get("shelfName"),
                        "displayType": product.get("displayType"),
                        "averageWeight": product.get("averageWeight"),
                        "bulkBuyLimit": product.get("bulkBuyLimit"),
                        "isForSale": product.get("isForSale"),
                        "media": json.dumps(product.get("media")),
                        "status": product.get("status"),
                        "productType": product.get("productType"),
                        "images": json.dumps(product.get("images")),
                        "details/details": details.get("details"),
                        "details/packSize": json.dumps(details.get("packSize")),
                        "allergenInfo": json.dumps(details.get("allergenInfo")),
                        "nutritionInfo": json.dumps(details.get("nutritionInfo")),
                        "price.actual": price_data.get("actual"),
                        "price.unitPrice": price_data.get("unitPrice"),
                        "price.unitOfMeasure": price_data.get("unitOfMeasure"),
                        "price.sellPrice": price_data.get("sellPrice"),
                        "price.wasPrice": price_data.get("wasPrice"),
                        "price.percentageSaved": price_data.get("percentageSaved")
                    }

                    if first_row:
                        writer = csv.DictWriter(f_out, fieldnames=result.keys())
                        writer.writeheader()
                        first_row = False

                    if writer:
                        writer.writerow(result)
            else:
                print(f"❌ {i+1} - HTTP {response.status_code}")
        except Exception as e:
            print(f"⚠️ Hiba ID: {pid} – {e}")

        # Idő és becslés
        elapsed = time.time() - start_time
        avg_per_item = elapsed / (i - start_index + 1)
        remaining = total - (i - start_index + 1)
        eta_sec = int(remaining * avg_per_item)
        eta_str = str(timedelta(seconds=eta_sec)).split('.')[0]

        print(f"✅ {i+1}/{start_index + total} | {round((i - start_index + 1) / total * 100, 1)}% | Várható hátralévő idő: {eta_str}")

