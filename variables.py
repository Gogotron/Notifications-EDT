prefix = "$""

BASE_URL = "https://apogee.u-bordeaux.fr/edt-st/Licence1/Semestre2/"
URL_MINF_A3	  = BASE_URL+"g254484.xml"
URL_MINF_A5   = BASE_URL+"g254486.xml"
URL_MINF_B5   = BASE_URL+"g301648.xml"
URL_PYC_A3    = BASE_URL+"g303429.xml"
URL_CH_A2     = BASE_URL+"g254353.xml"
URL_SI_A1     = BASE_URL+"g302805.xml"
URL_SV_A1     = BASE_URL+"g299833.xml"

URL_MINF_A    = BASE_URL+"g254481.xml"
URL_MINF_B    = BASE_URL+"g301643.xml"
URL_CMI_ISI   = BASE_URL+"g301653.xml"
URL_CMI_OPTIM = BASE_URL+"g347963.xml"

PI_URLS = [URL_MINF_A3, URL_MINF_A5, URL_MINF_B5, URL_PYC_A3, URL_CH_A2, URL_SI_A1, URL_SV_A1]
MI_URLS = [URL_MINF_A, URL_MINF_B, URL_CMI_ISI, URL_CMI_OPTIM]

channel = 802640238664351826
role_ids = (
	802575166831067166,  #A1
	802575212280807494,  #A2
	802575231691915344,  #A3
	802575247391064075,  #A4
	802575284070514688,  #A5
	802573383924449280,  #A6
	802573021222928414,  #B1
	802573125212045332,  #B2
	802573213602283521,  #B3
	802573271320887306,  #B4
	802573341495132222,  #B5
	802578798444675113,  #ISI
	802579017102000158,  #OPTIM
)
role_mentions = tuple(map(lambda role_id: f"<@&{role_id}>", role_ids))

group_to_mention = {
	'MINF201 SERIE A (Maths/Info)': role_mentions[0:6],
	'MINF201 SERIE B (Maths/Info)': role_mentions[6:11],
	'MINF201 GROUPE A1 (Maths/Info)': role_mentions[0:1],
	'MINF201 GROUPE A2 (Maths/Info)': role_mentions[1:2],
	'MINF201 GROUPE A3 (Maths/Info)': role_mentions[2:3],
	'MINF201 GROUPE A4 (Maths/Info)': role_mentions[3:4],
	'MINF201 GROUPE A5 (Maths/Info)': role_mentions[4:5],
	'MINF201 GROUPE A6 (Maths/Info)': role_mentions[5:6],
	'MINF201 GROUPE B1 (Maths/Info)': role_mentions[6:7],
	'MINF201 GROUPE B2 (Maths/Info)': role_mentions[7:8],
	'MINF201 GROUPE B4 (Maths/Info)': role_mentions[9:10],
	'MINF201 GROUPE B5 (Maths/Info)': role_mentions[10:11],
	'MINF201 GROUPE A11 (Maths/Info)': role_mentions[0:1],
	'MINF201 GROUPE A12 (Maths/Info)': role_mentions[0:1],
	'MINF201 GROUPE A21 (Maths/Info)': role_mentions[1:2],
	'MINF201 GROUPE A22 (Maths/Info)': role_mentions[1:2],
	'MINF201 GROUPE A31 (Maths/Info)': role_mentions[2:3],
	'MINF201 GROUPE A32 (Maths/Info)': role_mentions[2:3],
	'MINF201 GROUPE A41 (Maths/Info)': role_mentions[3:4],
	'MINF201 GROUPE A42 (Maths/Info)': role_mentions[3:4],
	'MINF201 GROUPE A51 (Maths/Info)': role_mentions[4:5],
	'MINF201 GROUPE A52 (Maths/Info)': role_mentions[4:5],
	'MINF201 GROUPE A61 (Maths/Info)': role_mentions[5:6],
	'MINF201 GROUPE B11 (Maths/Info)': role_mentions[6:7],
	'MINF201 GROUPE B12 (Maths/Info)': role_mentions[6:7],
	'MINF201 GROUPE B21 (Maths/Info)': role_mentions[7:8],
	'MINF201 GROUPE B22 (Maths/Info)': role_mentions[7:8],
	'MINF201 GROUPE B41 (Maths/Info)': role_mentions[9:10],
	'MINF201 GROUPE B42 (Maths/Info)': role_mentions[9:10],
	'MINF201 GROUPE B51 (Maths/Info)': role_mentions[10:11],
	'MINF201 GROUPE B52 (Maths/Info)': role_mentions[10:11],
	'CMI ISI201 GROUPE A1': role_mentions[11:12],
	'CMI OPTIM 201': role_mentions[12:13],
}

with open("help_text.txt", "r") as f:
	help_text = f.read().strip()
