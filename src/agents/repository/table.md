# 소설 창작 엔티티 구조 테이블

## 기본 엔티티 테이블

| 엔티티 | 정의 | 주요 속성 | 관계 |
|--------|------|-----------|------|
| 플롯(Plot) | 시퀀스를 갖고 있으며 시작, 중간, 결말 스레드로 구성된 이야기의 핵심 구조 | ID, 제목, 주제, 시간적 범위, 핵심 갈등 | 인물(다대다), 스레드(일대다), 세계관(다대일), 장(다대다) |
| 인물(Character) | 플롯에 참여하는 캐릭터들 | ID, 이름, 역할(주인공/조연/적대자 등), 목표, 성격, 배경 | 플롯(다대다), 이벤트(다대다) |
| 스레드(Thread) | 플롯을 구성하는 이야기 흐름 단위, 인물들 간 상호작용과 이벤트를 기록 | ID, 유형(시작/중간/결말), 설명, 순서 | 플롯(다대일), 이벤트(일대다), 씬(다대다) |
| 이벤트(Event) | 스레드 내에서 발생하는 구체적 사건 | ID, 설명, 발생 조건, 결과, 관련 인물 | 스레드(다대일), 인물(다대다) |
| 세계관(World) | 모든 플롯의 기반이 되는 배경 설정 | ID, 이름, 시대 설정, 지리적 특성, 사회 구조, 마법/과학 법칙 | 플롯(일대다) |
| 장(Chapter) | 소설의 구조적 단위 | ID, 제목, 순서, 주요 주제, 연결된 플롯 | 플롯(다대다), 씬(일대다), 리비전(일대다), 통합(다대일) |
| 씬(Scene) | 장을 구성하는 개별 상황 단위, 플롯의 스레드를 문학적 묘사 이전 상태로 구성 | ID, 설명, 장소, 시간, 참여 인물, 연결된 스레드/이벤트 | 장(다대일), 스레드(다대다), 묘사(일대다) |
| 묘사(Description) | 씬의 문학적 표현, 씬을 소설적 표현으로 변형 | ID, 내용, 톤, 스타일, 감각적 요소 | 씬(다대일) |
| 리비전(Revision) | 장의 편집/수정 버전, 각 장을 단편의 소설 형식으로 재구성 | ID, 버전, 변경 내용, 변경 이유, 날짜 | 장(다대일) |
| 통합(Integration) | 모든 장을 하나의 소설로 묶는 과정, 모든 리비전을 이어 하나의 소설로 엮음 | ID, 제목, 부제, 전체 구조, 연결 요소 | 장(일대다) |

## 엔티티 계층 구조

### 플롯 중심 엔티티 계층
- 플롯(Plot)
  - 인물(Character)
  - 스레드(Thread)
    - 이벤트(Event)

### 세계관 엔티티 계층
- 세계관(World)

### 장 중심 엔티티 계층
- 장(Chapter)
  - 씬(Scene)
    - 묘사(Description)
  - 리비전(Revision)

### 통합 엔티티 계층
- 통합(Integration)

## 주요 관계 다이어그램

```
세계관 ─────┐
            ↓
            플롯 ←───── 인물
             │
             ↓
          스레드 ←───── 이벤트
             │
             ↓
             씬
             │
             ↓
            묘사
             ↑
             │
            장 ────→ 리비전
             ↑
             │
            통합
```

## 데이터베이스 테이블 SQL 쿼리

### 기본 엔티티 테이블

```sql
-- 세계관(World) 테이블
CREATE TABLE World (
    world_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    time_period VARCHAR(255),
    geography TEXT,
    social_structure TEXT,
    laws_of_nature TEXT
);

-- 플롯(Plot) 테이블
CREATE TABLE Plot (
    plot_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    theme VARCHAR(255),
    time_span VARCHAR(255),
    core_conflict TEXT,
    world_id INT,
    FOREIGN KEY (world_id) REFERENCES World(world_id)
);

-- 인물(Character) 테이블
CREATE TABLE Character (
    character_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100),
    goal TEXT,
    personality TEXT,
    background TEXT
);

-- 스레드(Thread) 테이블
CREATE TABLE Thread (
    thread_id INT PRIMARY KEY,
    type ENUM('beginning', 'middle', 'end'),
    description TEXT,
    sequence_number INT,
    plot_id INT,
    FOREIGN KEY (plot_id) REFERENCES Plot(plot_id)
);

-- 이벤트(Event) 테이블
CREATE TABLE Event (
    event_id INT PRIMARY KEY,
    description TEXT,
    conditions TEXT,
    outcome TEXT,
    thread_id INT,
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id)
);

-- 장(Chapter) 테이블
CREATE TABLE Chapter (
    chapter_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    sequence_number INT,
    main_theme TEXT,
    integration_id INT,
    FOREIGN KEY (integration_id) REFERENCES Integration(integration_id)
);

-- 씬(Scene) 테이블
CREATE TABLE Scene (
    scene_id INT PRIMARY KEY,
    description TEXT,
    location VARCHAR(255),
    time VARCHAR(255),
    chapter_id INT,
    FOREIGN KEY (chapter_id) REFERENCES Chapter(chapter_id)
);

-- 묘사(Description) 테이블
CREATE TABLE Description (
    description_id INT PRIMARY KEY,
    content TEXT,
    tone VARCHAR(100),
    style VARCHAR(100),
    sensory_elements TEXT,
    scene_id INT,
    FOREIGN KEY (scene_id) REFERENCES Scene(scene_id)
);

-- 리비전(Revision) 테이블
CREATE TABLE Revision (
    revision_id INT PRIMARY KEY,
    version VARCHAR(50),
    changes TEXT,
    reason TEXT,
    date DATE,
    chapter_id INT,
    FOREIGN KEY (chapter_id) REFERENCES Chapter(chapter_id)
);

-- 통합(Integration) 테이블
CREATE TABLE Integration (
    integration_id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    subtitle VARCHAR(255),
    overall_structure TEXT,
    connecting_elements TEXT
);
```

### 관계 테이블 (다대다 관계)

```sql
-- 플롯-인물 관계 테이블
CREATE TABLE Plot_Character (
    plot_id INT,
    character_id INT,
    PRIMARY KEY (plot_id, character_id),
    FOREIGN KEY (plot_id) REFERENCES Plot(plot_id),
    FOREIGN KEY (character_id) REFERENCES Character(character_id)
);

-- 인물-이벤트 관계 테이블
CREATE TABLE Character_Event (
    character_id INT,
    event_id INT,
    role_in_event VARCHAR(100),
    PRIMARY KEY (character_id, event_id),
    FOREIGN KEY (character_id) REFERENCES Character(character_id),
    FOREIGN KEY (event_id) REFERENCES Event(event_id)
);

-- 스레드-씬 관계 테이블
CREATE TABLE Thread_Scene (
    thread_id INT,
    scene_id INT,
    PRIMARY KEY (thread_id, scene_id),
    FOREIGN KEY (thread_id) REFERENCES Thread(thread_id),
    FOREIGN KEY (scene_id) REFERENCES Scene(scene_id)
);

-- 플롯-장 관계 테이블
CREATE TABLE Plot_Chapter (
    plot_id INT,
    chapter_id INT,
    PRIMARY KEY (plot_id, chapter_id),
    FOREIGN KEY (plot_id) REFERENCES Plot(plot_id),
    FOREIGN KEY (chapter_id) REFERENCES Chapter(chapter_id)
);
```

### 샘플 쿼리

```sql
-- 특정 세계관에 속하는 모든 플롯 검색
SELECT p.* FROM Plot p
WHERE p.world_id = ?;

-- 특정 인물이 관여한 모든 이벤트 검색
SELECT e.* FROM Event e
JOIN Character_Event ce ON e.event_id = ce.event_id
WHERE ce.character_id = ?;

-- 특정 플롯의 시작-중간-끝 스레드 순서대로 검색
SELECT t.* FROM Thread t
WHERE t.plot_id = ?
ORDER BY t.sequence_number;

-- 특정 장의 모든 씬과 그 묘사 검색
SELECT s.*, d.* FROM Scene s
LEFT JOIN Description d ON s.scene_id = d.scene_id
WHERE s.chapter_id = ?
ORDER BY s.scene_id;

-- 특정 장의 리비전 이력 검색
SELECT r.* FROM Revision r
WHERE r.chapter_id = ?
ORDER BY r.date DESC;

-- 통합에 포함된 모든 장 순서대로 검색
SELECT c.* FROM Chapter c
WHERE c.integration_id = ?
ORDER BY c.sequence_number;
``` 