import glob
import os
import re
import csv

csv.field_size_limit(1024 * 1024 * 1024)


MAIN_FOLDER = "./../../../data/markets_data/"


def get_current_dir_name():
    return os.path.basename(os.getcwd()).lower()


def generate_filename(y_base, date_str: str, extension=".csv"):
    x = get_current_dir_name()
    return f"{MAIN_FOLDER}{x}_{y_base}_{date_str}{extension}"


def read_latest_file(y_base: str, extension=".csv"):
    x = get_current_dir_name()
    pattern = f"{MAIN_FOLDER}{x}_{y_base}_*{extension}"
    candidates = glob.glob(pattern)
    if not candidates:
        raise FileNotFoundError(f"Nincs fajl: {pattern}")

    latest = max(candidates, key=os.path.getmtime)
    match = re.search(rf"{re.escape(x)}_{re.escape(y_base)}_(\d{{8}}_\d{{6}}){re.escape(extension)}", latest)
    if not match:
        raise ValueError("Nem sikerult datumot kinyerni a fajlnevbol.")
    date_str = match.group(1)

    print(f"Fajl kivalasztva: {latest} (datum: {date_str})")
    return latest, date_str


important_columns = [
    "search_result_id",
    "search_page",
    "search_rank",
    "search_price",
    "search_is_available",
    "search_score",
    "detail_enriched",
    "article_key",
    "variant_key",
    "bundle_key",
    "variant_id",
    "bundle_id",
    "detail_store_id",
    "selected_delivery_mode",
    "selected_fulfillment_type",
    "customer_buyable",
    "fetch_category_path",
    "fetch_category_name",
    "fetch_category_paths",
    "fetch_category_names",
    "article.bettyArticleId.bettyArticleId",
    "article.bettyArticleId.articleNumber",
    "article.food",
    "article.foodNonFood",
    "article.brandName",
    "article.anonymousVisible",
    "article.anonymousSearchable",
    "variant.bettyVariantId.articleNumber",
    "variant.bettyVariantId.variantNumber",
    "variant.bettyVariantId.bettyVariantId",
    "variant.description",
    "variant.group.mainGroupName",
    "variant.group.groupName",
    "variant.group.subGroupName",
    "variant.categoryIds",
    "variant.categories",
    "variant.availability",
    "variant.imageUrl",
    "variant.imageUrlS",
    "variant.imageUrlL",
    "variant.logos",
    "variant.anonymousVisible",
    "variant.anonymousSearchable",
    "bundle.details",
    "bundle.bundleId.bettyBundleId",
    "bundle.bundleId.bettyVariantId",
    "bundle.bundleId.variantNumber",
    "bundle.bundleId.articleNumber",
    "bundle.bundleId.bundleNumber",
    "bundle.group.mainGroupName",
    "bundle.group.groupName",
    "bundle.group.subGroupName",
    "bundle.categories",
    "bundle.availability",
    "bundle.displayId",
    "bundle.customerDisplayId",
    "bundle.eanNumber",
    "bundle.description",
    "bundle.variantText",
    "bundle.bundleSize",
    "bundle.isWeightArticle",
    "bundle.isBuyMorePayLessArticle",
    "bundle.brandName",
    "bundle.ownBrand",
    "bundle.emptiesArticleNumber",
    "bundle.bundleVolume",
    "bundle.grossWeight",
    "bundle.imageUrl",
    "bundle.imageUrlS",
    "bundle.imageUrlL",
    "bundle.longDescription",
    "bundle.contentData",
    "bundle.contentData.netPieceWeight.value",
    "bundle.contentData.netPieceWeight.uom",
    "bundle.weightPerPiece",
    "bundle.weightPerPiece.value",
    "bundle.weightPerPiece.uom",
    "bundle.basePriceFactor",
    "bundle.basePriceContent",
    "bundle.basePriceContentMeasureUnit",
    "bundle.packagingType",
    "bundle.customerAvailability",
    "bundle.showCustomerAvailability",
    "bundle.gtins",
    "bundle.anonymousVisible",
    "bundle.anonymousSearchable",
    "store.country",
    "store.storeId",
    "store.delisted",
    "store.anonymousSearchable",
    "store.anonymousVisible",
    "price.finalPrice",
    "price.shelfPrice",
    "price.basePrice",
    "price.listNetPrice",
    "price.listGrossPrice",
    "price.deliveryPrice",
    "price.kgNet",
    "price.kgGross",
    "price.netPrice",
    "price.grossPrice",
    "price.currency",
    "price.vatPercent",
    "price.valid",
    "price.priceHiddenReason",
    "price.finalPricesInfo.sumGross",
    "price.finalPricesInfo.articleGross",
    "price.finalPricesInfo.articleWithTaxesGross",
    "price.finalPricesInfo.emptiesGross",
    "price.finalPricesInfo.singleSumGross",
    "price.finalPricesInfo.singleItemGross",
    "price.finalPricesInfo.avgPerUnitSumGross",
    "price.grossStrikeThrough",
    "price.strikeThrough",
    "price.appliedAdjustments",
    "price.applicablePromos",
    "price.availablePromotions",
    "price.promotionLabels",
    "price.dnrInfo",
    "price.summaryDnrInfo",
    "price.basePriceData.unit",
    "price.basePriceData.contentUnits",
    "price.basePriceData.pricePerUnit.grossPrice",
    "price.averagePerUnit",
]

input_file_name, input_date = read_latest_file("all_data")
output_file_name = generate_filename("filtered_data", input_date)

with open(input_file_name, mode="r", encoding="utf-8-sig", newline="") as infile, open(
    output_file_name, mode="w", encoding="utf-8", newline=""
) as outfile:
    reader = csv.DictReader(infile)
    fieldnames = [column for column in important_columns if column in (reader.fieldnames or [])]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()

    row_count = 0
    for row in reader:
        writer.writerow({column: row.get(column, "") for column in fieldnames})
        row_count += 1
        if row_count % 1000 == 0:
            print(f"{row_count} Metro sor szurve...")

print(f"{row_count} Metro sor szurve")
print(f"Lenyeges Metro oszlopokat tartalmazo fajl mentve ide: {output_file_name}")
