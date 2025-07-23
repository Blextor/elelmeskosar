import requests

url = "https://xapi.tesco.com/"

headers = {
    "accept": "application/json",
    "accept-language": "hu-HU",
    "content-type": "application/json",
    "language": "hu-HU",
    "origin": "https://bevasarlas.tesco.hu",
    "priority": "u=1, i",
    "referer": "https://bevasarlas.tesco.hu/groceries/hu-HU/shop/zoldseg.-gyumolcs/all?sortBy=relevance&page=3&count=48&_gl=1*1gc52kd*_up*MQ..*_ga*NDAzMjcxMjg0LjE3NTMwMjI1ODI.*_ga_SMN6XWLPM9*czE3NTMwMjI1ODEkbzEkZzAkdDE3NTMwMjI1ODEkajYwJGwwJGgxODY0NTE0Mzky",
    "region": "HU",
    "sec-ch-ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "traceid": "c478434a-25ff-46d6-995c-e1c4f356f436:65d06d98-53d2-4fcd-9ade-f6b3f5292d23",
    "trkid": "c478434a-25ff-46d6-995c-e1c4f356f436",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "x-apikey": "TvOSZJHlEk0pjniDGQFAc9Q59WGAR4dA"
}

payload = [
    {
        "operationName": "GetCategoryProducts",
        "variables": {
            "page": 3,
            "includeRestrictions": True,
            "includeVariations": True,
            "showDepositReturnCharge": True,
            "count": 48,
            "facet": "b;WiVDMyVCNmxkcyVDMyVBOWcuJTIwZ3klQzMlQkNtJUMzJUI2bGNz",
            "configs": [
                {
                    "featureKey": "dynamic_filter",
                    "params": [
                        {"name": "enable", "value": "true"}
                    ]
                }
            ],
            "filterCriteria": [
                {
                    "name": "0",
                    "values": ["groceries"]
                }
            ],
            "appliedFacetArgs": [],
            "sortBy": "relevance"
        },
        "extensions": {
            "mfeName": "mfe-plp"
        },
        "query": """query GetCategoryProducts($facet: ID, $page: Int = 1, $count: Int, $sortBy: String, $offset: Int, $favourites: Boolean, $configs: [ConfigArgType], $filterCriteria: [filterCriteria], $includeRestrictions: Boolean = true, $includeVariations: Boolean = true, $mediaExperiments: BrowseSearchConfig, $showDepositReturnCharge: Boolean = false, $appliedFacetArgs: [AppliedFacetArgs]) {
  category(
    page: $page
    count: $count
    configs: $configs
    sortBy: $sortBy
    offset: $offset
    facet: $facet
    favourites: $favourites
    config: $mediaExperiments
    filterCriteria: $filterCriteria
    appliedFacetArgs: $appliedFacetArgs
  ) {
    pageInformation: info {
      ...PageInformation
      __typename
    }
    results {
      node {
        ... on MPProduct {
          ...ProductItem
          __typename
        }
        ... on FNFProduct {
          ...ProductItem
          __typename
        }
        ... on ProductType {
          ...ProductItem
          __typename
        }
        __typename
      }
      __typename
    }
    facetLists: facetGroups {
      ...FacetLists
      __typename
    }
    facets {
      ...facet
      __typename
    }
    options {
      sortBy
      __typename
    }
    __typename
  }
}

fragment ProductItem on ProductInterface {
  typename: __typename
  ... on ProductType {
    context {
      type
      ... on ProductContextOfferType {
        linkTo
        offerType
        __typename
      }
      __typename
    }
    __typename
  }
  ... on MPProduct {
    context {
      type
      ... on ProductContextOfferType {
        linkTo
        offerType
        __typename
      }
      __typename
    }
    seller {
      id
      name
      __typename
    }
    fulfilment(deliveryOptions: BEST) {
      __typename
      ... on ProductDeliveryType {
        end
        charges {
          value
          __typename
        }
        __typename
      }
    }
    variations {
      ...Variation @include(if: $includeVariations)
      __typename
    }
    __typename
  }
  ... on FNFProduct {
    context {
      type
      ... on ProductContextOfferType {
        linkTo
        offerType
        __typename
      }
      __typename
    }
    variations {
      priceRange {
        minPrice
        maxPrice
        __typename
      }
      ...Variation @include(if: $includeVariations)
      __typename
    }
    __typename
  }
  id
  tpnb
  tpnc
  gtin
  adId
  baseProductId
  title
  brandName
  shortDescription
  defaultImageUrl
  superDepartmentId
  media {
    defaultImage {
      aspectRatio
      __typename
    }
    __typename
  }
  quantityInBasket
  superDepartmentName
  departmentId
  departmentName
  aisleId
  aisleName
  shelfId
  shelfName
  displayType
  productType
  charges @include(if: $showDepositReturnCharge) {
    ... on ProductDepositReturnCharge {
      __typename
      amount
    }
    __typename
  }
  averageWeight
  bulkBuyLimit
  maxQuantityAllowed: bulkBuyLimit
  groupBulkBuyLimit
  bulkBuyLimitMessage
  bulkBuyLimitGroupId
  timeRestrictedDelivery
  restrictedDelivery
  isForSale
  isInFavourites
  isNew
  isRestrictedOrderAmendment
  status
  maxWeight
  minWeight
  increment
  details {
    components {
      ...Competitors
      ...AdditionalInfo
      __typename
    }
    __typename
  }
  catchWeightList {
    price
    weight
    default
    __typename
  }
  price {
    price: actual
    unitPrice
    unitOfMeasure
    actual
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
    __typename
  }
  restrictions @include(if: $includeRestrictions) {
    type
    isViolated
    message
    __typename
  }
  reviews {
    stats {
      noOfReviews
      overallRating
      overallRatingRange
      __typename
    }
    __typename
  }
  modelMetadata {
    name
    version
    __typename
  }
}

fragment Competitors on CompetitorsInfo {
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

fragment AdditionalInfo on AdditionalInfo {
  isLowEverydayPricing
  __typename
}

fragment Variation on VariationsType {
  products {
    id
    baseProductId
    variationAttributes {
      attributeGroup
      attributeGroupData {
        name
        value
        attributes {
          name
          value
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
  __typename
}

fragment FacetLists on ProductListFacetsType {
  __typename
  category
  categoryId
  facets {
    facetId: id
    facetName: name
    binCount: count
    isSelected: selected
    __typename
  }
}

fragment PageInformation on ListInfoType {
  totalCount: total
  pageNo: page
  pageId
  count
  pageSize
  matchType
  offset
  query {
    searchTerm
    actualTerm
    __typename
  }
  __typename
}

fragment facet on FacetInterface {
  __typename
  id
  name
  type
  ... on FacetListType {
    id
    name
    listValues: values {
      name
      value
      isSelected
      count
      __typename
    }
    multiplicity
    metadata {
      description
      footerText
      linkText
      linkUrl
      __typename
    }
    __typename
  }
  ... on FacetMultiLevelType {
    id
    name
    multiLevelValues: values {
      children {
        count
        name
        value
        isSelected
        __typename
      }
      appliedValues {
        isSelected
        name
        value
        __typename
      }
      __typename
    }
    multiplicity
    metadata {
      description
      footerText
      linkText
      linkUrl
      __typename
    }
    __typename
  }
  ... on FacetRangeType {
    rangeValues: values {
      appliedMax
      appliedMin
      stepper
      min
      max
      __typename
    }
    __typename
  }
  ... on FacetBooleanType {
    booleanValues: values {
      count
      isSelected
      value
      name
      __typename
    }
    __typename
  }
}
"""  # Rövidítve
    }
]

response = requests.post(url, headers=headers, json=payload)

print(response.status_code)
print(response.json())
