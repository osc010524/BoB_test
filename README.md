# BoB_test


서버 구동 -> 어드민 계정으로 로그인 ->유저 계정 생성 -> 테스트 -> 재부팅 (DB write) -> 어드민 계정 테스트
if 어드민 계정 테스트 성공 => 파일 손상 X
elif 어드민 계정 테스트 실패 => 파일 손상

파일손상 -> DB 백업하여 저장 후 분석
