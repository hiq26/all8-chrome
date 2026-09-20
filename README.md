# ALL8 수집기

[최신 선공개 버전 다운로드](https://github.com/hiq26/all8-chrome/releases/download/latest-prerelease/all8-prerelease.zip)

압축을 해제한 뒤 확장 프로그램 관리 화면에서 개발자 모드를 켜고 **압축해제된 확장 프로그램 로드**로 설치하세요. 선공개 버전은 자동 업데이트되지 않습니다.

[버전별 릴리즈](https://github.com/hiq26/all8-chrome/releases) · [Windows Aside 연결 프로그램](https://github.com/hiq26/all8-aside-bridge/releases)

## 배포 관리

버전별 `vX.Y.Z` 릴리즈에 production `all8-X.Y.Z.zip` 파일을 업로드하고 프리릴리즈로 게시합니다. 새 태그는 기본 브랜치의 최신 커밋에서 생성하세요.

`Update prerelease download` workflow는 게시·수정·삭제 시 가장 높은 버전의 공개 프리릴리즈를 선택하여 `latest-prerelease` 채널의 `all8-prerelease.zip`을 갱신합니다. staging ZIP과 정식 릴리즈는 선택하지 않습니다. 원본 SHA-256과 ZIP 내부 manifest 버전을 검증합니다. Actions에서 수동 실행도 가능합니다. 채널 릴리즈 자체도 프리릴리즈이며 GitHub의 정식 latest를 대체하지 않습니다.

원본 ZIP은 릴리즈를 게시하기 전에 업로드하세요. 게시 후 Assets만 교체한 경우에는 workflow를 수동 실행하세요. 기존 태그가 workflow 추가 이전 커밋을 가리키는 경우에도 수동 실행이 필요합니다.
