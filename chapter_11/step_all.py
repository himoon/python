#######################################
# 1. 필요모듈
#######################################
import step_0
import step_1_1
import step_1_2
import step_1_3
import step_2_1
import step_2_2
import step_3_1
import step_3_2
import step_3_3
import step_3_4

#######################################
# 2. 환경설정
#######################################
pass

#######################################
# 3. 기본함수
#######################################
pass


#######################################
# 4. 메인함수
#######################################
def main():
    step_1_1.main()
    step_1_2.main()
    step_1_3.main()
    step_2_1.main()
    step_2_2.main()
    step_3_1.main()
    step_3_2.main()
    step_3_3.main()
    step_3_4.main()


#######################################
# 5. 실행
#######################################
if __name__ == "__main__":
    step_0.init_output_folder()
    step_0.clear_output_folder()
    main()
