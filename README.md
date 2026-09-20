# ALL8 수집기

[최신 선공개 버전 다운로드](https://github.com/hiq26/all8-chrome/releases/latest/download/all8-latest.zip)

**선공개**는 Chrome 웹스토어 심사 전에 사용자에게 공개하는 GitHub **Latest 정식 릴리즈**입니다. GitHub Pre-release는 개발용으로, 웹 다운로드에 연결하지 않습니다.

압축을 해제한 뒤 확장 프로그램 관리 화면에서 개발자 모드를 켜고 **압축해제된 확장 프로그램 로드**로 설치하세요. ZIP 설치는 자동 업데이트되지 않습니다.

[버전별 릴리즈](https://github.com/hiq26/all8-chrome/releases) · [Windows Aside 연결 프로그램](https://github.com/hiq26/all8-aside-bridge/releases)

## 배포 관리

`vX.Y.Z` 릴리즈에 production `all8-X.Y.Z.zip` 파일을 먼저 업로드합니다. 일반 사용자에게 공개할 버전은 Pre-release를 끄고 Latest로 지정합니다. 개발용 버전은 Pre-release로 유지합니다.

`Update Latest download` workflow는 GitHub `/releases/latest`가 선택한 릴리즈에 `all8-latest.zip`과 SHA256SUMS.txt를 추가합니다. 원본 SHA-256과 ZIP manifest를 검증하며, 정식 Latest 지정과 릴리즈 상태는 변경하지 않습니다. 개발용 Pre-release 이벤트는 건너뜁니다.

새 태그는 workflow가 있는 기본 브랜치 최신 커밋에서 생성하세요. 기존 태그가 workflow 추가 이전 커밋을 가리키거나 게시 후 Assets만 변경한 경우 Actions에서 수동 실행하세요.
