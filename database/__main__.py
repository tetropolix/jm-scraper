import sys
from sqlalchemy.exc import IntegrityError
from app import profileModels, authModels, productsModels
from app.extensions import db
from os import environ
from app import create_app


US_SIZES = [
    "1",
    "1.5",
    "2",
    "2.5",
    "3",
    "3.5",
    "4",
    "4.5",
    "5",
    "5.5",
    "6",
    "6.5",
    "7",
    "7.5",
    "8",
    "8.5",
    "9",
    "9.5",
    "10",
    "10.5",
    "11",
    "11.5",
    "12",
    "12.5",
    "13",
    "13.5",
    "14",
    "14.5",
    "15",
    "15.5",
    "16",
    "16.5",
    "17",
    "17.5",
    "18",
    "18.5",
    "19",
    "19.5",
    "20",
]
UK_SIZES = [
    "1",
    "1.5",
    "2",
    "2.5",
    "3",
    "3.5",
    "4",
    "4.5",
    "5",
    "5.5",
    "6",
    "6.5",
    "7",
    "7.5",
    "8",
    "8.5",
    "9",
    "9.5",
    "10",
    "10.5",
    "11",
    "11.5",
    "12",
    "12.5",
    "13",
    "13.5",
    "14",
    "14.5",
    "15",
    "15.5",
    "16",
    "16.5",
    "17",
    "17.5",
    "18",
    "18.5",
    "19",
    "19.5",
    "20",
]
CM_SIZES = [
    "1",
    "1.5",
    "2",
    "2.5",
    "3",
    "3.5",
    "4",
    "4.5",
    "5",
    "5.5",
    "6",
    "6.5",
    "7",
    "7.5",
    "8",
    "8.5",
    "9",
    "9.5",
    "10",
    "10.5",
    "11",
    "11.5",
    "12",
    "12.5",
    "13",
    "13.5",
    "14",
    "14.5",
    "15",
    "15.5",
    "16",
    "16.5",
    "17",
    "17.5",
    "18",
    "18.5",
    "19",
    "19.5",
    "20",
]
EU_SIZES = [
    "25",
    "25.5",
    "26",
    "26.5",
    "27",
    "27.5",
    "28",
    "28.5",
    "29",
    "29.5",
    "30",
    "30.5",
    "31",
    "31.5",
    "32",
    "32.5",
    "33",
    "33.5",
    "34",
    "34.5",
    "35",
    "35.5",
    "36",
    "36.5",
    "37",
    "37.5",
    "38",
    "38.5",
    "39",
    "39.5",
    "40",
    "40.5",
    "41",
    "41.5",
    "42",
    "42.5",
    "43",
    "43.5",
    "44",
    "44.5",
    "45",
    "45.5",
    "46",
    "46.5",
    "47",
    "47.5",
    "48",
    "48.5",
    "49",
    "49.5",
    "50",
    "50.5",
    "51",
    "51.5",
    "52",
    "25 1/3",
    "26 1/3",
    "27 1/3",
    "28 1/3",
    "29 1/3",
    "30 1/3",
    "31 1/3",
    "32 1/3",
    "33 1/3",
    "34 1/3",
    "35 1/3",
    "36 1/3",
    "37 1/3",
    "38 1/3",
    "39 1/3",
    "40 1/3",
    "41 1/3",
    "42 1/3",
    "43 1/3",
    "44 1/3",
    "45 1/3",
    "46 1/3",
    "47 1/3",
    "48 1/3",
    "49 1/3",
    "50 1/3",
    "51 1/3",
    "52 1/3",
    "25 2/3",
    "26 2/3",
    "27 2/3",
    "28 2/3",
    "29 2/3",
    "30 2/3",
    "31 2/3",
    "32 2/3",
    "33 2/3",
    "34 2/3",
    "35 2/3",
    "36 2/3",
    "37 2/3",
    "38 2/3",
    "39 2/3",
    "40 2/3",
    "41 2/3",
    "42 2/3",
    "43 2/3",
    "44 2/3",
    "45 2/3",
    "46 2/3",
    "47 2/3",
    "48 2/3",
    "49 2/3",
    "50 2/3",
    "51 2/3",
    "52 2/3",
]
GENDERS = ["Man", "Woman", "Kids", "Unknown"]
ESHOPS = [
    {
        "domain": "https://www.footshop.sk",
        "eshop_logo_url": "https://www.footshop.sk/android-chrome-192x192.png",
    },
    {
        "domain": "https://www.sivasdescalzo.com",
        "eshop_logo_url": "https://www.sivasdescalzo.com/static/version1657875030/frontend/Svd/theme/en_US/images/logo.svg",
    },
    {
        "domain": "https://www.queens.sk",
        "eshop_logo_url": "https://www.queens.cz/assets/queens-min.svg",
    },
]


def addShoeSizeRecordsToSession():
    for usSize in US_SIZES:
        db.session.add(productsModels.ShoeSizeUs(value=usSize))
    for ukSize in UK_SIZES:
        db.session.add(productsModels.ShoeSizeUk(value=ukSize))
    for cmSize in CM_SIZES:
        db.session.add(productsModels.ShoeSizeCm(value=cmSize))
    for euSize in EU_SIZES:
        db.session.add(productsModels.ShoeSizeEu(value=euSize))


def addGenderRecordsToSession():
    for gender in GENDERS:
        db.session.add(productsModels.Gender(gender=gender))


def addEshopRecordsToSession():
    for eshop in ESHOPS:
        db.session.add(productsModels.Eshop(**eshop))


if __name__ == "__main__":
    ENVIRONMENT_TYPE = environ.get("ENV_TYPE")
    app = create_app(ENVIRONMENT_TYPE)
    with app.app_context():
        db.session.begin()
        try:
            db.create_all()
            addShoeSizeRecordsToSession()
            addGenderRecordsToSession()
            addEshopRecordsToSession()
            db.session.commit()
        except IntegrityError as e:
            print(str(e))
            db.session.rollback()
        db.session.close()
