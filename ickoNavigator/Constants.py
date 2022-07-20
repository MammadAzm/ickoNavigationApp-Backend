import datetime


# Constant Values Begin Here=================================================
gpsAccuracy = 10  # meters

R = 6378.137  # Earth Radius

INTERVALS = {
    "daily": datetime.timedelta(days=1).total_seconds(),
    "weekly": datetime.timedelta(days=7).total_seconds(),
    "monthly": datetime.timedelta(days=30).total_seconds(),
}

ALL_TARGETS = "all"

SITE_NOT_ESTIMATED_MESSAGE = "Site Not Found. Check Out GPS."



