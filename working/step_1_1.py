# 국토교통부_아파트매매 실거래 상세 자료 https://www.data.go.kr/data/15057511/openapi.do
# 법정동코드목록조회 https://www.code.go.kr/stdcode/regCodeL.do


import xml.etree.ElementTree as ET

import requests

import step_0

XML_OUTPUT = step_0.OUTPUT_FOLDER / "step_1_1.xml"


url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
params = {
    "serviceKey": step_0.API_KEY_DATA_GO,
    # "pageNo": "1",
    # "numOfRows": "10",
    "LAWD_CD": "11110",
    "DEAL_YMD": "202306",
}

resp = requests.get(url, params=params)
resp.content

step_0.init_output_folder()
with open(XML_OUTPUT, "w") as fp:
    fp.write(resp.text)

# root = ET.fromstring(resp.text)
# for child in root.iter():
#     print(child)
