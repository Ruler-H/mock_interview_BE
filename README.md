# 개발자 모의 기술 면접 지원 서비스
## 목차
[1. 목표와 기능](#1-목표와-기능)  
[2. 개발 기술 및 환경, 배포 URL](#2-개발-기술-및-환경-배포-url)  
[3. 기능 명세](#3-기능-명세)

## 1. 목표와 기능
### 1-1. 목표
- 개발자 준비 과정에서 필요한 기술 모의 면접에 관련된 전반의 준비를 지원하는 플랫폼

### 1-2. 기능
- ChatGPT API를 통한 각 분야별, 경력별 기술 면접 기능
- 모의 면접 진행이 가능하며 해당 질문의 의도나 질문에 대한 모범 답을 확인하는 기능
- 기술 면접과 관련된 질문을 받아 답변을 해주는 챗봇 기능

#### [Flow Chart]
<img src="./static/assets/images/flow_chart.png" width="100%">

## 2. 개발 기술 및 환경, 배포 URL
### 2-1. 개발 기술
#### [기술 - FE]  
<div>
    <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=white">
    <img src="https://img.shields.io/badge/html5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
    <img src="https://img.shields.io/badge/css3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
    <img src="https://img.shields.io/badge/bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white">
</div>

#### [기술 - BE]
<div>
    <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white">
    <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white">
</div>

#### [기술 - DB]
<img src="https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white">

### 2-2. 개발 환경
<div>
    <img src="https://img.shields.io/badge/amazonaws-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white">
    <img src="https://img.shields.io/badge/visualstudio-007ACC?style=for-the-badge&logo=visualstudio&logoColor=white">
    <img src="https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white">
</div>

### 2-3. 배포 URL
추가 필요

## 3. 기능 명세
### 3-1. 필수 요구사항
 - DRF 기반 API 구현
 - CBV 혹은 FBV를 사용
 - 회원가입 구현
 - 로그인 구현
 - ChatGPT로 요청하는 API를 Django 서버에서 요청하고 응답받아서 FE 서버에 응답
 - Chatbot API는 로그인 한 유저만 사용
 - user 당 1일 5회까지만 Chatbot 요청을 제한
 - 채팅 내용은 DB에 저장
 - 이전 채팅 내용을 조회할 수 있도록 구현
 - 이전 채팅 내용은 로그인한 본인만 확인 가능

### 3-2. 추가 요구사항
 - 개인 도메인 등록
 - FE, BE 서버 각각 배포(배포 시 https 추가)
 - OAuth 2.0을 이용한 Kakao, github 연결

### 3-3. 기능 목록



## 3. 프로젝트 구조와 개발 일정
### 3-1. 프로젝트 디렉터리 구조
