#######################################
# 1. 필요모듈
#######################################
import json

import geopandas as gpd
from datakart import Sgis

import step_0

#######################################
# 2. 환경설정
#######################################
API_KEY = "c45c510fe7854d5aae90"
API_SEC = "fde5af5e4362466b91fe"
STEP_2_1 = step_0.OUTPUT_DIR / "step_2_1.geojson"


#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    # https://sgis.kostat.go.kr/developer/html/newOpenApi/api/dataApi/addressBoundary.html#hadmarea
    api = Sgis(API_KEY, API_SEC)
    resp = api.hadm_area(adm_cd="11", low_search="1")
    gdf_resp: gpd.GeoDataFrame = gpd.read_file(json.dumps(resp))
    gdf_resp.set_crs("EPSG:5179", allow_override=True, inplace=True)
    gdf_result = gdf_resp.sort_values("adm_nm").reset_index(drop=True).filter(["adm_cd", "adm_nm", "geometry"])

    with open(STEP_2_1, "w", encoding="utf8") as fp:
        fp.write(gdf_result.to_json(drop_id=True, to_wgs84=True))


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    main()
