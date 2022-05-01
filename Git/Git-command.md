# Git Command
## mirror 
<sup> 새로판 깃계정이있는데, 그냥 원래쓰던거로 다시 옮기기로 결정했다.</sup>  
repository 를 이동 시킬 때 commit 등의 이력까지 같이 이동 시키는 방법

~~~
1. 복사할 리포지토리를 local에서 미러링 
$ git clone --mirror {기존 레파지토리 주소}

2. 미러링이 되면 <리포지토리> 폴더가 생기는데 해당 폴더로 이동
$ cd {기존 레파지토리 명}.git

3. 복사를 진행할 새 레포지토리 URL을 입력하여 push 한다.
$ git remote set-url --push origin {새로운 레파지토리 주소}

$ git push --mirror
~~~


## user/email 변경
<sup> 분명 커밋했는데, 반영은되지만 잔디가안심어지는 경우가있다.. 원인은  회사계정으로 되어있었다.</sup>
~~~
# 현재 name/email확인
$  git config --global user.name 
$  git config --global user.email

# name/email 변경
git config user.email jdy9436@naver.com
git config user.name "day0ung"
~~~


