# -*- coding: utf-8 -*-

from numpy import nan
from pathlib import Path


def format_title(title, subtitle=None, subtitle_font_size=14): 
    title = f'<b>{title}</b>' 
    if not subtitle: 
        return title 
    subtitle = f'<span style="font-size: {subtitle_font_size}px;">({subtitle})</span>' 
    return f'{title}<br>{subtitle}'

def find_files(name: str, path: Path):
    # if path is not a directory we do not need to iterate
    if all((path, path.is_file(), name in path.name)):
        yield path

    # if path is a folder iterate over all contained folders and files
    elif path and path.is_dir():
        for p in path.iterdir():
            # "yield from" is required for recursive generator functions (our find_files)
            yield from find_files(name=name, path=p.absolute())
    
indicators = [
    'PRCE_NA_NA_NA_CR_IMCO_USA_RDLRPBRL',
    'PRCE_NA_NA_NA_CR_IMCO_USA_NDLRPBRL',
    'CNSM_NA_LFL_NA_TOT_NA_USA_MILLBRLPDY',
    'SUP_PRD_NA_NA_CR_NA_USA_MILLBRLPDY',
    'TRAD_NA_LFL_TOT_NETIMP_NA_USA_MILLBRLPDY',  # trad_NA_lfl_NA_netimp_netimp_usa_millbrlpdy
    'PRCE_DELV_ELEP_NA_NG_NA_USA_RDLRPMCF',
    'PRCE_DELV_ELEP_NA_NG_NA_USA_NDLRPMCF',
    'CNSM_NA_ALLS_NA_NG_TOT_USA_TRLCF',
    'SUP_DPR_NA_NA_NG_TOT_USA_TRLCF',
    'TRAD_NETIMP_NA_NA_NG_NA_USA_TRLCF',
    'PRCE_NOM_ELEP_NA_STC_NA_NA_RDLRPMBTU',
    'PRCE_NOM_ELEP_NA_STC_NA_NA_NDLRPMBTU',
    'CNSM_NA_NA_NA_CL_NA_NA_MILLTON',
    'SUP_NA_NA_NA_CL_NA_NA_MILLTON',
    'PRCE_NA_ELEP_NA_EDU_NA_USA_RCNTPKWH',
    'PRCE_NA_ELEP_NA_EDU_NA_USA_NCNTPKWH',
    'CNSM_NA_ELEP_NA_ELS_NA_USA_BLNKWH', # GEN_NA_ELEP_NAG_NAG_NA_USA_BLNKWH
    'GEN_NA_ALLS_NA_SLR_NA_NA_BLNKWH',
    'GEN_NA_ALLS_NA_WND_NA_NA_BLNKWH',
    'GEN_NA_ELEP_NA_HYD_CNV_NA_BLNKWH',
    'GEN_NA_ELEP_TGE_CL_NA_USA_BLNKWH',
    'GEN_NA_ELEP_TGE_NG_NA_USA_BLNKWH',
    'GEN_NA_ELEP_TGE_NUP_NA_USA_BLNKWH',
    'CNSM_ENU_TEN_NA_TOT_NA_NA_QBTU',
    'CNSM_ENU_RES_NA_DELE_NA_NA_QBTU',
    'CNSM_ENU_COMM_NA_DELE_NA_NA_QBTU',
    'CNSM_ENU_IDAL_NA_DELE_NA_NA_QBTU',
    'CNSM_ENU_TRN_NA_DELE_NA_NA_QBTU',
    'EMI_CO2_NA_NA_NA_NA_NA_MILLMTCO2EQ',
    'INY_NA_NA_NA_TEN_NA_NA_THBTUPDLRGDP',
]

indicators_labels = [
    'Imported refiner acquisition cost of crude oil (real 2012$)',
    'Imported refiner acquisition cost of crude oil (nominal)',
    'Total petroleum and other liquids consumption',
    'Domestic crude oil production',
    'Petroleum net imports',
    'Natural gas price, electric power sector (real 2012$)',
    'Natural gas price, electric power sector (nominal)',
    'Total natural gas consumption',
    'Dry natural gas production',
    'Natural gas net imports',
    'Coal prices to electric generating plants (real 2012$)',
    'Coal prices to electric generating plants (nominal)',
    'Total coal consumption',
    'Coal production excluding waste coal',
    'Average electricity prices (real 2012$)',
    'Average electricity prices (nominal)',
    'Total electricity sales excluding direct use',
    'Solar net generation from all sectors',
    'Wind net generation from all sectors',
    'Conventional hydroelectric power net generation from all sectors',
    'Coal net generation from all sectors',
    'Natural gas net generation from all sectors',
    'Nuclear net generation from all sectors',
    'Total energy consumption from all sectors',
    'Total delivered residential energy consumption',
    'Total delivered commercial energy consumption',
    'Total delivered industrial energy consumption',
    'Total delivered transportation energy consumption',
    'Total energy-related carbon dioxide emissions',
    'Energy intensity',
]

titles_dict = dict(zip(indicators,indicators_labels))

meta_tags = [
    {
        "name": "author",
        "content": "U.S. Energy Information Administration (EIA)",
    },
    {
        "name": "subject",
         "content": "official energy statistics, data, analysis and forecasting",
    },
    {
        "name": "description",
        "content": "Energy Information Administration - EIA - Official Energy Statistics from the U.S. Government",
    },
    {
        "name":"agency", 
        "content": "EIA - Energy Information Administration",
    },
    {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1",
    },
    {
        "property": "og:type",
        "content": "website",
    },
    {
        "property": "og:title",
        "content": "EIA Benchmarking tool - U.S. Energy Information Administration (EIA)",
    },
    {
        "property": "og:description",
        "content": " ",
    },
    {
        "property": "og:image",
        "content": "https://www.eia.gov/about/images/eiabuglogo.jpg",
    },
    {
        "name": "robots",
        "content": "all",
    },
    {
        "property": "twitter:title",
        "content": "Tools to make life easier",
    },
    {
        "property": "twitter:description",
        "content": "Automate repetitive data analysis tasks and perform predictions and optimizations",
    },
    {
        "property": "twitter:image",
        "content": " ",
    },
]

units_dict = {
    'BLNKWH': 'billion kilowatthours', # keep
    'MILLBRLPDY': 'million barrels per day', # keep
    'MILLMTCO2EQ': 'mmtco2eq', # keep
    'MILLTON': 'million short tons', # keep
    'NCNTPKWH': 'nominal cents per kilowatthour', # keep
    'NDLRPBRL': 'nominal dollars per barrel', # keep
    'NDLRPMCF': 'nominal dollars per thousand cubic feet', # keep
    'NDLRPMBTU': 'nominal dollars per thousand Btu', # keep
    'RCNTPKWH': 'real cents per kilowatthour in 2012$', # keep
    'RDLRPBRL': 'real dollars per barrel in 2012$', # keep
    'RDLRPMCF': 'real dollars per thousand cubic feet in 2012$', # keep
    'RDLRPMBTU': 'real dollars per thousand Btu in 2012$', # keep
    'QBTU': 'quadrillion Btu', # keep
    'THBTUPDLRGDP': 'thousand Btu per dollar GDP', # keep
    'TRLCF': 'trillion cubic feet', # keep
}

case_name_labels_dict = {
    'ACTUAL': 'Actual',
    'HIGHMACHIGHZTC': 'High Macro and High Zero-Carbon Technology Cost',
    'HIGHMACLOWZTC': 'High Macro and Low Zero-Carbon Technology Cost',
    'HIGHMACRO': 'High Economic Growth',
    'HIGHOGS': 'High Oil and Gas Supply',
    'HIGHPRICE': 'High Oil Price',
    'HIGHUPIRA': 'High Uptake of Inflation Reduction Act',
    'HIGHZTC': 'High Zero-Carbon Technology Cost',
    'LOWMACHIGHZTC': 'Low Macro and High Zero-Carbon Technology Cost',
    'LOWMACLOWZTC': 'Low Macro and Low Zero-Carbon Technology Cost',
    'LOWMACRO': 'Low Economic Growth',
    'LOWOGS': 'Low Oil and Gas Supply',
    'LOWPRICE': 'Low Oil Price',
    'LOWUPIRA': 'Low Uptake of Inflation Reduction Act',
    'LOWZTC': 'Low Zero-Carbon Technology Cost',
    'NOIRA': 'No Inflation Reduction Act',
    'REFERENCE': 'Reference case',
}

sources_dict = {
    'ECI_NA_NA_NA_GDP_REAL_NA_BLNY09DLR': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy,<a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: GDPRVUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_NA_NA_NA_CR_IMCO_USA_NDLRPBRL': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: RAIMUUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_NA_NA_NA_CR_IMCO_USA_RDLRPBRL': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: RAIMUUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_NA_LFL_NA_TOT_NA_USA_MILLBRLPDY': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: PATCPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'SUP_PRD_NA_NA_CR_NA_USA_MILLBRLPDY': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: PAPRPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'TRAD_NA_LFL_TOT_NETIMP_NA_USA_MILLBRLPDY': 'PANIPUS' "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: PANIPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_DELV_ELEP_NA_NG_NA_USA_NDLRPMCF': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: NGEIUUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_DELV_ELEP_NA_NG_NA_USA_RDLRPMCF': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: NGEIUUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_NA_ALLS_NA_NG_TOT_USA_TRLCF': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: NGTCPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'SUP_DPR_NA_NA_NG_TOT_USA_TRLCF': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: NGPRPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'TRAD_NETIMP_NA_NA_NG_NA_USA_TRLCF': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: NGNIPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_NOM_ELEP_NA_STC_NA_NA_NDLRPMBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: CLERDUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_NOM_ELEP_NA_STC_NA_NA_RDLRPMBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: CLERDUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_NA_NA_NA_CL_NA_NA_MILLTON': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: CLTCPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'SUP_NA_NA_NA_CL_NA_NA_MILLTON': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: CLPRPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_NA_ELEP_NA_EDU_NA_USA_NCNTPKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: ESTCUUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'PRCE_NA_ELEP_NA_EDU_NA_USA_RCNTPKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: ESTCUUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_NA_ELEP_NA_ELS_NA_USA_BLNKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: ESTCPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'GEN_NA_ALLS_NA_SLR_NA_NA_BLNKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: SOETPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'GEN_NA_ALLS_NA_WND_NA_NA_BLNKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: WYETPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'GEN_NA_ELEP_NA_HYD_CNV_NA_BLNKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: HVETPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'GEN_NA_ELEP_TGE_CL_NA_USA_BLNKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: CLETPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'GEN_NA_ELEP_TGE_NG_NA_USA_BLNKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: NGETPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'GEN_NA_ELEP_TGE_NUP_NA_USA_BLNKWH': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: NUETPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_ENU_TEN_NA_TOT_NA_NA_QBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TETCBUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'EMI_CO2_NA_NA_NA_NA_NA_MILLMTCO2EQ': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TETCEUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'INY_NA_NA_NA_TEN_NA_NA_THBTUPDLRGDP': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TETCBUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'DMG_POP_NA_NA_NA_NA_NA_MILL': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TPOPPUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'ECI_INDX_NA_NA_GDP_NA_NA_Y09EQ1D3Z': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: GDPDIUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_ENU_TEN_NA_TOT_NA_NA_QBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TETCBUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_ENU_RES_NA_DELE_NA_NA_QBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TERCBUS and LORCBUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_ENU_COMM_NA_DELE_NA_NA_QBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TECCBUS and LOCCBUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_ENU_IDAL_NA_DELE_NA_NA_QBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TEICBUS and LOICBUS</a>; projections: Annual Energy Outlook, case projections from various editions",
    'CNSM_ENU_TRN_NA_DELE_NA_NA_QBTU': "Data source: Historical data are from the U.S. Energy Information Administration open data API (accessed June 2024), https://www.eia.gov/opendata/browser/total-energy, <a href='https://www.eia.gov/opendata/browser/total-energy'> annual series: TEACBUS and LOACBUS</a>; projections: Annual Energy Outlook, case projections from various editions",
}