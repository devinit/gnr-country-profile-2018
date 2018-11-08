#!/usr/bin/python
# -*- coding: utf-8 -*-

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import copy
import pandas as pd
import numbers
import re
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

blue = "#3D5163"
grey = "#C7D4E0"
orange = "#F68516"
light_blue = "#82C6BA"
lighter_blue = "#BFDFD4"

pdfmetrics.registerFont(TTFont('Arial', 'fonts/Arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'fonts/Arial-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Italic', 'fonts/Arial-Italic.ttf'))
addMapping('Arial', 0, 0, 'Arial')
addMapping('Arial', 0, 1, 'Arial-Italic')
addMapping('Arial', 1, 0, 'Arial-Bold')

style = getSampleStyleSheet()
blueParaBold = ParagraphStyle('blueParaBold', parent=style['BodyText'], textColor=blue, alignment=TA_LEFT, fontName="Arial-Bold")
blueParaBoldCenter = ParagraphStyle('blueParaBold', parent=style['BodyText'], textColor=blue, alignment=TA_CENTER, fontName="Arial-Bold")
blueParaStyle = ParagraphStyle('blueParaStyle', parent=style['BodyText'], textColor=blue, alignment=TA_LEFT)
offCourseStyle = ParagraphStyle('offCourseStyle', parent=style['BodyText'], textColor=orange, alignment=TA_LEFT)
progressStyle = ParagraphStyle('progressStyle', parent=style['BodyText'], textColor=lighter_blue, alignment=TA_LEFT)
onCourseStyle = ParagraphStyle('onCourseStyle', parent=style['BodyText'], textColor=light_blue, alignment=TA_LEFT)


def condStyle(progress):
    if progress == "On course":
        return onCourseStyle
    elif progress == "No progress or worsening":
        return offCourseStyle
    elif progress == "Some progress":
        return progressStyle
    else:
        return blueParaStyle

dataDictionary = {"Kenya": {}}
dataDictionary["Kenya"]["country"] = "Kenya"

dataDictionary["Kenya"]["table1"] = [
    [
        Paragraph("<b>Under-5 stunting</b>", style=blueParaBold),
        Paragraph("<b>Under-5 wasting</b>", style=blueParaBold),
        Paragraph("<b>Under-5 overweight</b>", style=blueParaBold),
        Paragraph("<b>WRA anaemia</b>", style=blueParaBold),
        Paragraph("<b>EBF</b>", style=blueParaBold)
     ],
    ["Off course, some progress", "On course", "Off course, no progress", "Off course", "On course"]
]

dataDictionary["Kenya"]["table1a"] = [
    [
        Paragraph("<b>Adult female obesity</b>", style=blueParaBold),
        Paragraph("<b>Adult male obesity</b>", style=blueParaBold),
        Paragraph("<b>Adult female diabetes</b>", style=blueParaBold),
        Paragraph("<b>Adult male diabetes</b>", style=blueParaBold)
     ],
    ["Off course, some progress", "On course", "Off course, no progress", "Off course"]
]

dataDictionary["Kenya"]["table2"] = [
    [
        Paragraph("<b>Coverage/practice indicator</b>", style=blueParaBold),
        Paragraph("<b>%</b>", style=blueParaBold),
        Paragraph("<b>Male</b>", style=blueParaBold),
        Paragraph("<b>Female</b>", style=blueParaBold),
        Paragraph("<b>Year</b>", style=blueParaBold)
     ],
    [u"Children 0\u201359 months with dirrhea who received zinc treatment", "8.1", "", "", "2014"],
    [u"Children 6\u201359 months who received vitamin A supplements in last 6 months", "71.7", "71.6", "71.9", "2014"],
    [u"Children 6\u201359 months given iron supplements in past 7 days", "2.7", "2.6", "2.7", "2014"],
    [Paragraph("Women with a birth in last five years who received iron and folic acid during their most recent pregnancy", style=blueParaStyle), "69.4", "", "", "2014"],
    ["Household consumption of adequately iodised salt", "99.5", "", "", "2014"],
]

dataDictionary["Kenya"]["table3"] = [
    [Paragraph("Mandatory legislation for salt iodisation", style=blueParaBold), "Yes"],
    [Paragraph(u"Sugar\u2013sweeted beverage tax", style=blueParaBold), "Yes"],
    [Paragraph("Multisectoral comprehensive nutrition plan", style=blueParaBold), "Yes"],
]

dataDictionary["Kenya"]["table4"] = [
    [
        Paragraph("Stunting", style=blueParaBoldCenter),
        Paragraph("Anaemia", style=blueParaBoldCenter),
        Paragraph("LBW", style=blueParaBoldCenter),
        Paragraph("Child overweight", style=blueParaBoldCenter),
        Paragraph("Exclusive breastfeeding", style=blueParaBoldCenter),
        Paragraph("Wasting", style=blueParaBoldCenter),
        Paragraph("Salt/sodium intake", style=blueParaBoldCenter),
        Paragraph("Blood pressure", style=blueParaBoldCenter),
        Paragraph("Diabetes", style=blueParaBoldCenter),
        Paragraph("Overweight adults and adolescents", style=blueParaBoldCenter),
    ],
    ["Yes", "Yes", "No", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes"]
]

dataDictionary["Kenya"]["table5"] = [
    [Paragraph("Gini index score<super>1</super>", style=blueParaBold), Paragraph("Gini index rank<super>2</super>", style=blueParaBold), "Year"], [51, 125, 2011]
]

dataDictionary["Kenya"]["table6"] = [
    ["Population (000)", format(12428, ",d"), 2015],
    ["Under-5 population (000)", format(1935, ",d"), 2015],
    ["Urban (%)", format(20, ",d"), 2015],
    [">65 years (%)", format(5, ",d"), 2015],
]

dataDictionary["Kenya"]["table7"] = [
    [Paragraph("Early childbearing: births by age 18 (%)<super>1</super>", style=blueParaBold), "33", "2011"],
    [Paragraph("Gender Inequality Index (score*)<super>2</super>", style=blueParaBold), "0.529", "2013"],
    [Paragraph("Gender Inequality Index (country rank)<super>2</super>", style=blueParaBold), "155", "2013"]
]
dataDictionary["Kenya"]["table8"] = [
    ["Physicians", "0.117", "2005"],
    ["Nurses and midwives", "1.306", "2005"],
    ["Community health workers", "0.188", "2005"]
]

# dataDictionary["Kenya"] = copy.deepcopy(dataDictionary["Kenya"])


def replaceDash(x):
    x = str(x)
    y = re.sub(r"((?:^|[^{])\d+)-(\d+[^}])", u"\\1\u2013\\2", x)
    return y
missingVals = [" ", ".", "", "Insufficient data to make assessment"]


def safeFormat(x, commas=False, precision=0, percent=False):
    if pd.isnull(x):
        return "NA"
    elif x in missingVals:
        return "NA"
    else:
        if percent:
            try:
                x = float(x) * 100
            except ValueError:
                return replaceDash(x)
        if not isinstance(x, numbers.Number):
            return replaceDash(x)
        if precision == 0:
            x = int(round(x, precision))
        else:
            x = round(x, precision)
        if commas:
            return format(x, ",")
        else:
            return x


def indicator(ctryDat, indicator):
    return ctryDat.loc[(ctryDat["indicator"] == indicator)].iloc[0]["value"]


def indicator_disagg(ctryDat, indicator, disagg, disagg_value=None):
    if disagg_value:
        return ctryDat.loc[(ctryDat["indicator"] == indicator) & (ctryDat["disaggregation"] == disagg) & (ctryDat["disagg.value"] == disagg_value)].iloc[0]["value"]
    else:
        return ctryDat.loc[(ctryDat["indicator"] == indicator) & (ctryDat["disaggregation"] == disagg)].iloc[0]["value"]


def year(ctryDat, indicator):
    return ctryDat.loc[(ctryDat["indicator"] == indicator)].iloc[0]["year"]

dat = pd.read_csv("data.csv")
for country in dataDictionary.keys():
    ctryDat = dat.loc[(dat.country == country)]
    dataDictionary[country]["country"] = country
    dataDictionary[country]["country_class"] = indicator(ctryDat, "country_class")
    dataDictionary[country]["burden_text"] = indicator(ctryDat, "burden_text")
    dataDictionary[country]["table1"][1] = [
        Paragraph(safeFormat(indicator(ctryDat, "under_5_stunting_track")), style=condStyle(indicator(ctryDat, "under_5_stunting_track"))),
        Paragraph(safeFormat(indicator(ctryDat, "under_5_wasting_track")), style=condStyle(indicator(ctryDat, "under_5_wasting_track"))),
        Paragraph(safeFormat(indicator(ctryDat, "under_5_overweight_track")), style=condStyle(indicator(ctryDat, "under_5_overweight_track"))),
        Paragraph(safeFormat(indicator(ctryDat, "wra_anaemia_track")), style=condStyle(indicator(ctryDat, "wra_anaemia_track"))),
        Paragraph(safeFormat(indicator(ctryDat, "ebf_track")), style=condStyle(indicator(ctryDat, "ebf_track"))),
    ]

    dataDictionary[country]["table1a"][1] = [
        Paragraph(safeFormat(indicator(ctryDat, "adult_fem_obesity_track")), style=condStyle(indicator(ctryDat, "adult_fem_obesity_track"))),
        Paragraph(safeFormat(indicator(ctryDat, "adult_mal_obesity_track")), style=condStyle(indicator(ctryDat, "adult_mal_obesity_track"))),
        Paragraph(safeFormat(indicator(ctryDat, "adult_fem_diabetes_track")), style=condStyle(indicator(ctryDat, "adult_fem_diabetes_track"))),
        Paragraph(safeFormat(indicator(ctryDat, "adult_mal_diabetes_track")), style=condStyle(indicator(ctryDat, "adult_mal_diabetes_track"))),
    ]

    dataDictionary[country]["table2"][1][1] = safeFormat(indicator_disagg(ctryDat, "diarrhea_zinc", "all"), percent=True)
    dataDictionary[country]["table2"][1][2] = safeFormat(indicator_disagg(ctryDat, "diarrhea_zinc", "gender", "Male"), percent=True)
    dataDictionary[country]["table2"][1][3] = safeFormat(indicator_disagg(ctryDat, "diarrhea_zinc", "gender", "Female"), percent=True)
    dataDictionary[country]["table2"][1][4] = safeFormat(year(ctryDat, "diarrhea_zinc"))

    dataDictionary[country]["table2"][2][1] = safeFormat(indicator_disagg(ctryDat, "vit_a", "all"), percent=True)
    dataDictionary[country]["table2"][2][2] = safeFormat(indicator_disagg(ctryDat, "vit_a", "gender", "Male"), percent=True)
    dataDictionary[country]["table2"][2][3] = safeFormat(indicator_disagg(ctryDat, "vit_a", "gender", "Female"), percent=True)
    dataDictionary[country]["table2"][2][4] = safeFormat(year(ctryDat, "vit_a"))

    dataDictionary[country]["table2"][3][1] = safeFormat(indicator_disagg(ctryDat, "iron_supp", "all"), percent=True)
    dataDictionary[country]["table2"][3][2] = safeFormat(indicator_disagg(ctryDat, "iron_supp", "gender", "Male"), percent=True)
    dataDictionary[country]["table2"][3][3] = safeFormat(indicator_disagg(ctryDat, "iron_supp", "gender", "Female"), percent=True)
    dataDictionary[country]["table2"][3][4] = safeFormat(year(ctryDat, "iron_supp"))

    dataDictionary[country]["table2"][4][1] = safeFormat(indicator_disagg(ctryDat, "iron_and_folic", "all"), percent=True)
    dataDictionary[country]["table2"][4][2] = safeFormat(indicator_disagg(ctryDat, "iron_and_folic", "gender", "Male"), percent=True)
    dataDictionary[country]["table2"][4][3] = safeFormat(indicator_disagg(ctryDat, "iron_and_folic", "gender", "Female"), percent=True)
    dataDictionary[country]["table2"][4][4] = safeFormat(year(ctryDat, "iron_and_folic"))

    dataDictionary[country]["table2"][5][1] = safeFormat(indicator_disagg(ctryDat, "iodised_salt", "all"), percent=True)
    dataDictionary[country]["table2"][5][2] = safeFormat(indicator_disagg(ctryDat, "iodised_salt", "gender", "Male"), percent=True)
    dataDictionary[country]["table2"][5][3] = safeFormat(indicator_disagg(ctryDat, "iodised_salt", "gender", "Female"), percent=True)
    dataDictionary[country]["table2"][5][4] = safeFormat(year(ctryDat, "iodised_salt"))

    dataDictionary[country]["table3"][0][1] = safeFormat(indicator(ctryDat, "salt_leg"))
    dataDictionary[country]["table3"][1][1] = safeFormat(indicator(ctryDat, "sugar_tax"))
    dataDictionary[country]["table3"][2][1] = safeFormat(indicator(ctryDat, "multi_sec"))

    dataDictionary[country]["table4"][1] = [
        safeFormat(indicator(ctryDat, "stunting_plan")),
        safeFormat(indicator(ctryDat, "anaemia_plan")),
        safeFormat(indicator(ctryDat, "LBW_plan")),
        safeFormat(indicator(ctryDat, "child_overweight_plan")),
        safeFormat(indicator(ctryDat, "EBF_plan")),
        safeFormat(indicator(ctryDat, "wasting_plan")),
        safeFormat(indicator(ctryDat, "sodium_plan")),
        safeFormat(indicator(ctryDat, "blood_pressure_plan")),
        safeFormat(indicator(ctryDat, "diabetes_plan")),
        safeFormat(indicator(ctryDat, "overweight_adults_adoles_plan")),
    ]

    dataDictionary[country]["table5"][1] = [
        safeFormat(indicator(ctryDat, "gini")),
        safeFormat(indicator(ctryDat, "gini_rank")),
        safeFormat(indicator(ctryDat, "gini_year"))
    ]

    dataDictionary[country]["table6"][0][1] = safeFormat(indicator(ctryDat, "population"), True)
    dataDictionary[country]["table6"][0][2] = safeFormat(year(ctryDat, "population"))
    dataDictionary[country]["table6"][1][1] = safeFormat(indicator(ctryDat, "u5_pop"), True)
    dataDictionary[country]["table6"][1][2] = safeFormat(year(ctryDat, "u5_pop"))
    dataDictionary[country]["table6"][2][1] = safeFormat(indicator(ctryDat, "urban_percent"))
    dataDictionary[country]["table6"][2][2] = safeFormat(year(ctryDat, "urban_percent"))
    dataDictionary[country]["table6"][3][1] = safeFormat(indicator(ctryDat, "65_years"), True)
    dataDictionary[country]["table6"][3][2] = safeFormat(year(ctryDat, "65_years"))

    dataDictionary[country]["table7"][0][1] = safeFormat(indicator(ctryDat, "early_childbearing_prev"))
    dataDictionary[country]["table7"][0][2] = safeFormat(year(ctryDat, "early_childbearing_prev"))
    dataDictionary[country]["table7"][1][1] = safeFormat(indicator(ctryDat, "gender_inequality_score"), False, 3)
    dataDictionary[country]["table7"][1][2] = safeFormat(year(ctryDat, "gender_inequality_score"))
    dataDictionary[country]["table7"][2][1] = safeFormat(indicator(ctryDat, "gender_inequality_rank"))
    dataDictionary[country]["table7"][2][2] = safeFormat(year(ctryDat, "gender_inequality_rank"))

    dataDictionary[country]["table8"][0][1] = safeFormat(indicator(ctryDat, "physicians"), False, 3)
    dataDictionary[country]["table8"][0][2] = safeFormat(year(ctryDat, "physicians"))
    dataDictionary[country]["table8"][1][1] = safeFormat(indicator(ctryDat, "nurses_and_midwives"), False, 3)
    dataDictionary[country]["table8"][1][2] = safeFormat(year(ctryDat, "nurses_and_midwives"))
    dataDictionary[country]["table8"][2][1] = safeFormat(indicator(ctryDat, "community_health_workers"), False, 3)
    dataDictionary[country]["table8"][2][2] = safeFormat(year(ctryDat, "community_health_workers"))

generic_style = [
    ('TEXTCOLOR', (0, 0), (-1, -1), blue),
    ('BACKGROUND', (0, 0), (-1, -1), "white"),
    ('LINEABOVE', (0, 0), (-1, 0), 1, blue),
    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
    ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
    ('LINEBELOW', (0, -1), (-1, -1), 1, grey)
]

tableStyles = {}
tableStyles["table1"] = [
    ('TEXTCOLOR', (0, 0), (-1, -1), blue),
    ('BACKGROUND', (0, 0), (-1, -1), "transparent"),
    ('ALIGN', (0, 0), (-1, -1), "LEFT"),
    ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
    ('FONTNAME', (0, 0), (-1, 0), "Arial-Bold")
]
tableStyles["table1a"] = tableStyles["table1"]
tableStyles["table2"] = generic_style + [
    ('FONTNAME', (0, 0), (-1, 0), "Arial-Bold"),
    ('LINEABOVE', (0, 1), (-1, 1), 1, blue),
    ('LINEABOVE', (0, 2), (-1, 2), 1, grey),
    ('LINEABOVE', (0, 3), (-1, 3), 1, grey),
    ('LINEABOVE', (0, 4), (-1, 4), 1, grey),
    ('LINEABOVE', (0, 5), (-1, 5), 1, grey),
]
tableStyles["table3"] = generic_style
tableStyles["table4"] = generic_style + [
    ('TEXTCOLOR', (0, 0), (-1, -1), blue),
    ('BACKGROUND', (0, 0), (-1, -1), "white"),
    ('ALIGN', (0, 0), (-1, -1), "CENTER"),
    ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
    ('LINEAFTER', (0, 0), (0, -1), 1, blue),
    ('LINEAFTER', (1, 0), (1, -1), 1, blue),
    ('LINEAFTER', (2, 0), (2, -1), 1, blue),
    ('LINEAFTER', (3, 0), (3, -1), 1, blue),
    ('LINEAFTER', (4, 0), (4, -1), 1, blue),
    ('LINEAFTER', (5, 0), (5, -1), 1, blue),
    ('LINEAFTER', (6, 0), (6, -1), 1, blue),
    ('LINEAFTER', (7, 0), (7, -1), 1, blue),
    ('LINEAFTER', (8, 0), (8, -1), 1, blue),
]
tableStyles["table5"] = generic_style + [
    ('FONTNAME', (0, 0), (-1, 0), "Arial-Bold"),
    ('LINEABOVE', (0, 1), (-1, 1), 1, blue)
]
tableStyles["table6"] = generic_style + [
    ('LINEABOVE', (0, 1), (-1, 1), 1, grey),
    ('LINEABOVE', (0, 2), (-1, 2), 1, grey),
    ('LINEABOVE', (0, 3), (-1, 3), 1, grey),
    ('FONTNAME', (0, 0), (0, -1), "Arial-Bold")
]
tableStyles["table7"] = generic_style
tableStyles["table8"] = generic_style
