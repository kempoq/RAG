"""
graph_loader.py
Загрузка тестовых документов в Neo4j Knowledge Graph.
"""

from typing import List, Dict, Any
from langchain_neo4j import Neo4jGraph


# ---------------------------------------------------------------------------
# Тестовые данные (10 документов на основе OCR)
# ---------------------------------------------------------------------------

SAMPLE_DOCS: List[Dict[str, Any]] = [
    {
        "doc_id": "DOC_001",
        "title": "Гидрометаллургическая переработка уранового сырья",
        "source_type": "textbook",
        "entities": [
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Кислотное выщелачивание", "domain": "U", "stage_type": "leaching", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "H2SO4", "class": "acid", "hazard_class": "2"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "NaClO3", "class": "oxidant"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "pH", "unit": "", "control_type": "constraint", "criticality_level": "high"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "Температура", "unit": "°C", "control_type": "input", "criticality_level": "high"}},
            {"type": "Оборудование", "props": {"name": "Пачук", "functional_type": "reactor", "scale": "industrial", "material_req": "wood"}},
            {"type": "Оборудование", "props": {"name": "Стержневая мельница Доминион", "functional_type": "mill", "scale": "industrial"}},
            {"type": "Руда_Сырье", "props": {"name": "Песчаник урановый", "ore_type": "sandstone", "target_elements": ["U"], "grade_range": "0.1-0.3%"}},
        ],
        "relations": [
            {"source": ("Технологический_Процесс", "Кислотное выщелачивание"), "target": ("Химический_Реагент", "H2SO4"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "leachant", "dosage": "31 кг/т руды"}},
            {"source": ("Технологический_Процесс", "Кислотное выщелачивание"), "target": ("Химический_Реагент", "NaClO3"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "oxidant", "dosage": "0.9 кг/т"}},
            {"source": ("Параметр_Среды", "pH"), "target": ("Технологический_Процесс", "Кислотное выщелачивание"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "critical", "range": "1.5-2.5"}},
            {"source": ("Параметр_Среды", "Температура"), "target": ("Технологический_Процесс", "Кислотное выщелачивание"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "positive", "range": "75-80"}},
            {"source": ("Технологический_Процесс", "Кислотное выщелачивание"), "target": ("Оборудование", "Пачук"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"mode": "batch", "duration": "48 ч"}},
            {"source": ("Руда_Сырье", "Песчаник урановый"), "target": ("Технологический_Процесс", "Кислотное выщелачивание"), "type": "ПОДВЕРГАЕТСЯ", "props": {"efficiency": "94-95%"}},
        ],
    },
    {
        "doc_id": "DOC_002",
        "title": "Сорбционное извлечение урана из осветленных растворов",
        "source_type": "textbook",
        "entities": [
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Ионный обмен", "domain": "U", "stage_type": "sorption", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Десорбция", "domain": "U", "stage_type": "elution", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "Анионит АВ-17", "class": "extractant", "hazard_class": "3"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "HNO3", "class": "acid", "hazard_class": "2"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "NH3", "class": "base", "hazard_class": "2"}},
            {"type": "Оборудование", "props": {"name": "Сорбционная колонна", "functional_type": "column", "scale": "industrial", "material_req": "rubber-lined"}},
            {"type": "Оборудование", "props": {"name": "Десорбционная колонна", "functional_type": "column", "scale": "industrial"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "pH", "unit": "", "control_type": "constraint", "criticality_level": "high"}},
        ],
        "relations": [
            {"source": ("Технологический_Процесс", "Ионный обмен"), "target": ("Химический_Реагент", "Анионит АВ-17"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "sorbent", "capacity": "70 кг U/м³"}},
            {"source": ("Технологический_Процесс", "Десорбция"), "target": ("Химический_Реагент", "HNO3"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "eluant", "concentration": "азотная кислота"}},
            {"source": ("Параметр_Среды", "pH"), "target": ("Технологический_Процесс", "Ионный обмен"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "optimum", "range": "2.0"}},
            {"source": ("Технологический_Процесс", "Ионный обмен"), "target": ("Оборудование", "Сорбционная колонна"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"mode": "continuous", "size": "2.4×3.6 м"}},
            {"source": ("Технологический_Процесс", "Десорбция"), "target": ("Оборудование", "Десорбционная колонна"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"mode": "batch", "cycle": "2 ч"}},
        ],
    },
    {
        "doc_id": "DOC_003",
        "title": "Технологическая схема завода Денисон майнз",
        "source_type": "report",
        "entities": [
            {"type": "Завод_Установка", "props": {"name": "Денисон майнз", "location": "Канада", "operator": "Denison Mines", "capacity_tpd": "7200", "ore_type_processed": "кварцево-галечные конгломераты"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Рудногалечное измельчение", "domain": "U", "stage_type": "grinding", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Противоточная декантация", "domain": "U", "stage_type": "washing", "maturity_level": "industrial"}},
            {"type": "Оборудование", "props": {"name": "Щековая дробилка", "functional_type": "crusher", "scale": "industrial", "size": "0.914×1.22 м"}},
            {"type": "Оборудование", "props": {"name": "Колосниковый виброгрохот", "functional_type": "classifier", "scale": "industrial"}},
            {"type": "Оборудование", "props": {"name": "Сгуститель", "functional_type": "thickener", "scale": "industrial", "size": "30 м диаметр"}},
            {"type": "Руда_Сырье", "props": {"name": "Кварцево-галечный конгломерат", "ore_type": "conglomerate", "target_elements": ["U"], "grade_range": "0.1-0.13%"}},
        ],
        "relations": [
            {"source": ("Завод_Установка", "Денисон майнз"), "target": ("Технологический_Процесс", "Рудногалечное измельчение"), "type": "ВНЕДРЯЕТ", "props": {"year": "1967", "efficiency": "снижение стоимости на 0.2 долл/т"}},
            {"source": ("Завод_Установка", "Денисон майнз"), "target": ("Технологический_Процесс", "Противоточная декантация"), "type": "ВНЕДРЯЕТ", "props": {"stage": "washing"}},
            {"source": ("Завод_Установка", "Денисон майнз"), "target": ("Руда_Сырье", "Кварцево-галечный конгломерат"), "type": "ПЕРЕРАБАТЫВАЕТ", "props": {"source": "рудник", "blending": "усреднение"}},
            {"source": ("Технологический_Процесс", "Рудногалечное измельчение"), "target": ("Оборудование", "Щековая дробилка"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"stage": "primary"}},
            {"source": ("Технологический_Процесс", "Противоточная декантация"), "target": ("Оборудование", "Сгуститель"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"count": "10", "configuration": "2 нитки по 5"}},
        ],
    },
    {
        "doc_id": "DOC_004",
        "title": "Жидкостная экстракция урана",
        "source_type": "textbook",
        "entities": [
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Жидкостная экстракция", "domain": "U", "stage_type": "extraction", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Реэкстракция", "domain": "U", "stage_type": "stripping", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "Аламин-336", "class": "extractant", "hazard_class": "3"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "Керосин", "class": "solvent", "hazard_class": "3"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "(NH4)2SO4", "class": "salt", "hazard_class": "4"}},
            {"type": "Оборудование", "props": {"name": "Смеситель-отстойник", "functional_type": "separator", "scale": "industrial", "size": "1.5×1.8 м"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "O:V соотношение", "unit": "", "control_type": "input", "criticality_level": "medium"}},
            {"type": "Материальный_Поток", "props": {"name": "Экстракт", "phase_state": "organic", "functional_role": "extract", "typical_composition_ref": "5% амина в керосине"}},
            {"type": "Материальный_Поток", "props": {"name": "Рафинат", "phase_state": "aqueous", "functional_role": "raffinate", "typical_composition_ref": "после экстракции"}},
        ],
        "relations": [
            {"source": ("Технологический_Процесс", "Жидкостная экстракция"), "target": ("Химический_Реагент", "Аламин-336"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "extractant", "concentration": "5%"}},
            {"source": ("Технологический_Процесс", "Жидкостная экстракция"), "target": ("Химический_Реагент", "Керосин"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "diluent"}},
            {"source": ("Технологический_Процесс", "Реэкстракция"), "target": ("Химический_Реагент", "(NH4)2SO4"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "stripping_agent", "concentration": "250 г/л"}},
            {"source": ("Параметр_Среды", "O:V соотношение"), "target": ("Технологический_Процесс", "Жидкостная экстракция"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "critical", "value": "3:1"}},
            {"source": ("Технологический_Процесс", "Жидкостная экстракция"), "target": ("Оборудование", "Смеситель-отстойник"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"stages": "4", "mode": "counter-current"}},
            {"source": ("Технологический_Процесс", "Жидкостная экстракция"), "target": ("Материальный_Поток", "Экстракт"), "type": "ГЕНЕРИРУЕТ", "props": {"composition": "4.5 г U3O8/л"}},
            {"source": ("Технологический_Процесс", "Жидкостная экстракция"), "target": ("Материальный_Поток", "Рафинат"), "type": "ГЕНЕРИРУЕТ", "props": {"destination": "сорбционное отделение"}},
        ],
    },
    {
        "doc_id": "DOC_005",
        "title": "Завод в Лисбоне (Юта, США)",
        "source_type": "case_study",
        "entities": [
            {"type": "Завод_Установка", "props": {"name": "Завод в Лисбоне", "location": "США, Юта", "operator": "Рио-Алгом майнз", "capacity_tpd": "750", "commissioning_year": "1972"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Содовое автоклавное выщелачивание", "domain": "U", "stage_type": "leaching", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Химическое осаждение", "domain": "U", "stage_type": "precipitation", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "Na2CO3", "class": "base", "hazard_class": "4"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "NH4OH", "class": "base", "hazard_class": "2"}},
            {"type": "Оборудование", "props": {"name": "Автоклав", "functional_type": "reactor", "scale": "industrial", "material_req": "steel"}},
            {"type": "Оборудование", "props": {"name": "Барабанный фильтр", "functional_type": "filter", "scale": "industrial", "size": "1.8×1.8 м"}},
            {"type": "Руда_Сырье", "props": {"name": "Песчаник с прослоями сланца", "ore_type": "sandstone", "target_elements": ["U"], "grade_range": "0.1-0.3%"}},
        ],
        "relations": [
            {"source": ("Завод_Установка", "Завод в Лисбоне"), "target": ("Технологический_Процесс", "Содовое автоклавное выщелачивание"), "type": "ВНЕДРЯЕТ", "props": {"year": "1972", "expansion": "1975"}},
            {"source": ("Завод_Установка", "Завод в Лисбоне"), "target": ("Руда_Сырье", "Песчаник с прослоями сланца"), "type": "ПЕРЕРАБАТЫВАЕТ", "props": {"source": "подземный рудник", "recovery": "95%"}},
            {"source": ("Технологический_Процесс", "Содовое автоклавное выщелачивание"), "target": ("Химический_Реагент", "Na2CO3"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "leaching_agent"}},
            {"source": ("Технологический_Процесс", "Химическое осаждение"), "target": ("Химический_Реагент", "NH4OH"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "precipitant", "pH": "7.2"}},
            {"source": ("Технологический_Процесс", "Химическое осаждение"), "target": ("Оборудование", "Барабанный фильтр"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"stage": "final"}},
            {"source": ("Завод_Установка", "Завод в Лисбоне"), "target": ("Технологический_Процесс", "Кислотное выщелачивание"), "type": "ВНЕДРЯЕТ", "props": {"note": "модернизация"}},
        ],
    },
    {
        "doc_id": "DOC_006",
        "title": "Кучное выщелачивание урановых руд",
        "source_type": "textbook",
        "entities": [
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Кучное выщелачивание", "domain": "U", "stage_type": "heap_leaching", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "H2SO4", "class": "acid", "hazard_class": "2"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "Плотность орошения", "unit": "л/(м²·ч)", "control_type": "input", "criticality_level": "high"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "Высота штабеля", "unit": "м", "control_type": "design", "criticality_level": "medium"}},
            {"type": "Оборудование", "props": {"name": "Перфорированные трубы", "functional_type": "distributor", "scale": "industrial"}},
            {"type": "Оборудование", "props": {"name": "Сборный зумпф", "functional_type": "collector", "scale": "industrial"}},
            {"type": "Завод_Установка", "props": {"name": "Сопка Рудная", "location": "Россия", "capacity_tpd": "N/A", "ore_type_processed": "урановые руды"}},
            {"type": "Завод_Установка", "props": {"name": "Комсомольская залежь", "location": "Россия", "capacity_tpd": "N/A", "ore_type_processed": "урановые руды"}},
            {"type": "Завод_Установка", "props": {"name": "Кировское", "location": "Россия", "capacity_tpd": "N/A", "ore_type_processed": "урановые руды"}},
        ],
        "relations": [
            {"source": ("Технологический_Процесс", "Кучное выщелачивание"), "target": ("Химический_Реагент", "H2SO4"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "leachant", "application": "орошение"}},
            {"source": ("Параметр_Среды", "Плотность орошения"), "target": ("Технологический_Процесс", "Кучное выщелачивание"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "critical", "range": "10-12"}},
            {"source": ("Параметр_Среды", "Высота штабеля"), "target": ("Технологический_Процесс", "Кучное выщелачивание"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "design", "range": "3.2-7.0"}},
            {"source": ("Технологический_Процесс", "Кучное выщелачивание"), "target": ("Оборудование", "Перфорированные трубы"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"function": "орошение"}},
            {"source": ("Технологический_Процесс", "Кучное выщелачивание"), "target": ("Оборудование", "Сборный зумпф"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"function": "сбор продуктивного раствора"}},
            {"source": ("Завод_Установка", "Сопка Рудная"), "target": ("Технологический_Процесс", "Кучное выщелачивание"), "type": "ВНЕДРЯЕТ", "props": {"stack_height": "4.0 м", "irrigation": "12 л/(м²·ч)"}},
            {"source": ("Завод_Установка", "Кировское"), "target": ("Технологический_Процесс", "Кучное выщелачивание"), "type": "ВНЕДРЯЕТ", "props": {"stack_height": "7.0 м", "irrigation": "10 л/(м²·ч)"}},
        ],
    },
    {
        "doc_id": "DOC_007",
        "title": "Подготовка руд к гидрометаллургической переработке",
        "source_type": "textbook",
        "entities": [
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Дробление", "domain": "general", "stage_type": "crushing", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Измельчение", "domain": "general", "stage_type": "grinding", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Грохочение", "domain": "general", "stage_type": "screening", "maturity_level": "industrial"}},
            {"type": "Оборудование", "props": {"name": "Молотковая дробилка", "functional_type": "crusher", "scale": "industrial", "size": "0.81×1.03 м"}},
            {"type": "Оборудование", "props": {"name": "Конусная дробилка", "functional_type": "crusher", "scale": "industrial", "size": "2.1 м"}},
            {"type": "Оборудование", "props": {"name": "Реечный классификатор", "functional_type": "classifier", "scale": "industrial", "size": "3.15×9.75 м"}},
            {"type": "Оборудование", "props": {"name": "Гидроциклон", "functional_type": "classifier", "scale": "industrial", "size": "254 мм"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "Плотность пульпы", "unit": "% твердого", "control_type": "input", "criticality_level": "high"}},
        ],
        "relations": [
            {"source": ("Технологический_Процесс", "Дробление"), "target": ("Оборудование", "Молотковая дробилка"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"capacity": "110 т/ч", "product_size": "-12 мм"}},
            {"source": ("Технологический_Процесс", "Дробление"), "target": ("Оборудование", "Конусная дробилка"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"stage": "secondary"}},
            {"source": ("Технологический_Процесс", "Измельчение"), "target": ("Оборудование", "Реечный классификатор"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"circuit": "closed"}},
            {"source": ("Технологический_Процесс", "Измельчение"), "target": ("Оборудование", "Гидроциклон"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"function": "classification"}},
            {"source": ("Параметр_Среды", "Плотность пульпы"), "target": ("Технологический_Процесс", "Измельчение"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "critical", "range": "58-75"}},
        ],
    },
    {
        "doc_id": "DOC_008",
        "title": "Осаждение урана и получение концентрата",
        "source_type": "textbook",
        "entities": [
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Химическое осаждение", "domain": "U", "stage_type": "precipitation", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Фильтрация", "domain": "U", "stage_type": "solid_liquid_separation", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Сушка", "domain": "U", "stage_type": "drying", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "MgO", "class": "base", "hazard_class": "4"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "NaOH", "class": "base", "hazard_class": "2"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "H2O2", "class": "oxidant", "hazard_class": "2"}},
            {"type": "Оборудование", "props": {"name": "Фильтрпресс", "functional_type": "filter", "scale": "industrial", "size": "1420×1420 мм"}},
            {"type": "Оборудование", "props": {"name": "Паровая сушилка", "functional_type": "dryer", "scale": "industrial", "size": "1.8×1.8 м"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "pH", "unit": "", "control_type": "constraint", "criticality_level": "high"}},
        ],
        "relations": [
            {"source": ("Технологический_Процесс", "Химическое осаждение"), "target": ("Химический_Реагент", "MgO"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "precipitant", "dosage": "0.7 кг/т"}},
            {"source": ("Технологический_Процесс", "Химическое осаждение"), "target": ("Химический_Реагент", "NaOH"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "precipitant", "product": "диуранат натрия"}},
            {"source": ("Технологический_Процесс", "Химическое осаждение"), "target": ("Химический_Реагент", "H2O2"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "precipitant", "product": "пероксид урана"}},
            {"source": ("Параметр_Среды", "pH"), "target": ("Технологический_Процесс", "Химическое осаждение"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "critical", "range": "7.0-7.2"}},
            {"source": ("Технологический_Процесс", "Фильтрация"), "target": ("Оборудование", "Фильтрпресс"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"cake_moisture": "55%"}},
            {"source": ("Технологический_Процесс", "Сушка"), "target": ("Оборудование", "Паровая сушилка"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"temperature": "157°C", "duration": "40 мин"}},
            {"source": ("Технологический_Процесс", "Химическое осаждение"), "target": ("Технологический_Процесс", "Фильтрация"), "type": "ГЕНЕРИРУЕТ", "props": {"product": "пульпа концентрата"}},
        ],
    },
    {
        "doc_id": "DOC_009",
        "title": "Завод Сплит Рок (Вестерн ньюклеар)",
        "source_type": "case_study",
        "entities": [
            {"type": "Завод_Установка", "props": {"name": "Сплит Рок", "location": "США", "operator": "Western Nuclear", "capacity_tpd": "N/A", "commissioning_year": "1966"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Сорбция из пульпы", "domain": "U", "stage_type": "resin_in_pulp", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "FeSO4", "class": "reductant", "hazard_class": "4"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "MgO", "class": "base", "hazard_class": "4"}},
            {"type": "Оборудование", "props": {"name": "Сорбционный чан с мешалкой", "functional_type": "reactor", "scale": "industrial", "size": "3.9×4.2 м"}},
            {"type": "Оборудование", "props": {"name": "Эрлифт", "functional_type": "pump", "scale": "industrial"}},
            {"type": "Параметр_Среды", "props": {"symbol_or_name": "ОВП", "unit": "мВ", "control_type": "constraint", "criticality_level": "high"}},
            {"type": "Руда_Сырье", "props": {"name": "Сцементированный песчаник", "ore_type": "sandstone", "target_elements": ["U", "Mo"], "grade_range": "0.2% U"}},
        ],
        "relations": [
            {"source": ("Завод_Установка", "Сплит Рок"), "target": ("Технологический_Процесс", "Сорбция из пульпы"), "type": "ВНЕДРЯЕТ", "props": {"year": "1966", "note": "непрерывная сорбция"}},
            {"source": ("Завод_Установка", "Сплит Рок"), "target": ("Руда_Сырье", "Сцементированный песчаник"), "type": "ПЕРЕРАБАТЫВАЕТ", "props": {"moisture": "8-15%", "recovery": ">99%"}},
            {"source": ("Технологический_Процесс", "Сорбция из пульпы"), "target": ("Химический_Реагент", "FeSO4"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "reductant", "dosage": "1.8 г/т"}},
            {"source": ("Технологический_Процесс", "Сорбция из пульпы"), "target": ("Химический_Реагент", "MgO"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "pH_adjuster", "dosage": "0.20 кг/т"}},
            {"source": ("Параметр_Среды", "ОВП"), "target": ("Технологический_Процесс", "Сорбция из пульпы"), "type": "ВЛИЯЕТ_НА", "props": {"effect": "critical", "value": "500 мВ"}},
            {"source": ("Технологический_Процесс", "Сорбция из пульпы"), "target": ("Оборудование", "Сорбционный чан с мешалкой"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"count": "10", "configuration": "2 нитки по 5"}},
            {"source": ("Технологический_Процесс", "Сорбция из пульпы"), "target": ("Оборудование", "Эрлифт"), "type": "РАЗМЕЩАЕТСЯ_В", "props": {"function": "перекачка пульпы"}},
        ],
    },
    {
        "doc_id": "DOC_010",
        "title": "Комплексное использование уранового сырья",
        "source_type": "textbook",
        "entities": [
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Извлечение молибдена", "domain": "U-Mo", "stage_type": "byproduct_recovery", "maturity_level": "industrial"}},
            {"type": "Технологический_Процесс", "props": {"canonical_name": "Извлечение ванадия", "domain": "U-V", "stage_type": "byproduct_recovery", "maturity_level": "industrial"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "Na2S", "class": "reductant", "hazard_class": "3"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "Ca(OH)2", "class": "base", "hazard_class": "3"}},
            {"type": "Химический_Реагент", "props": {"formula_or_name": "(NH4)2CO3", "class": "salt", "hazard_class": "4"}},
            {"type": "Материальный_Поток", "props": {"name": "Хвосты медных руд", "phase_state": "solid", "functional_role": "waste", "typical_composition_ref": "150 г U3O8/т"}},
            {"type": "Руда_Сырье", "props": {"name": "Уран-ванадиевые руды", "ore_type": "sandstone", "target_elements": ["U", "V"], "grade_range": "variable"}},
        ],
        "relations": [
            {"source": ("Технологический_Процесс", "Извлечение молибдена"), "target": ("Химический_Реагент", "Na2S"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "precipitant", "dosage": "0.200 кг/кг U"}},
            {"source": ("Технологический_Процесс", "Извлечение молибдена"), "target": ("Химический_Реагент", "Ca(OH)2"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "precipitant", "dosage": "1.600 кг/кг U"}},
            {"source": ("Технологический_Процесс", "Извлечение ванадия"), "target": ("Химический_Реагент", "(NH4)2CO3"), "type": "ИСПОЛЬЗУЕТ", "props": {"role": "leaching_agent", "product": "молибдат аммония"}},
            {"source": ("Технологический_Процесс", "Извлечение молибдена"), "target": ("Технологический_Процесс", "Кислотное выщелачивание"), "type": "ОПИСЫВАЕТСЯ", "props": {"relation": "sequential"}},
            {"source": ("Материальный_Поток", "Хвосты медных руд"), "target": ("Технологический_Процесс", "Кислотное выщелачивание"), "type": "ПОТРЕБЛЯЕТ", "props": {"source": "медное производство", "U_content": "150 г/т"}},
        ],
    },
]

# ---------------------------------------------------------------------------
# Ключи уникальности по типам узлов
# ---------------------------------------------------------------------------

UNIQUE_KEYS: Dict[str, str] = {
    "Технологический_Процесс": "canonical_name",
    "Химический_Реагент": "formula_or_name",
    "Параметр_Среды": "symbol_or_name",
    "Оборудование": "name",
    "Документ": "doc_id",
    "Руда_Сырье": "name",
    "Завод_Установка": "name",
    "Материальный_Поток": "name",
}


# ---------------------------------------------------------------------------
# Ограничения схемы
# ---------------------------------------------------------------------------

CONSTRAINTS = [
    "CREATE CONSTRAINT process_canonical IF NOT EXISTS FOR (n:Технологический_Процесс) REQUIRE n.canonical_name IS UNIQUE",
    "CREATE CONSTRAINT reagent_canonical IF NOT EXISTS FOR (n:Химический_Реагент) REQUIRE n.formula_or_name IS UNIQUE",
    "CREATE CONSTRAINT param_canonical IF NOT EXISTS FOR (n:Параметр_Среды) REQUIRE n.symbol_or_name IS UNIQUE",
    "CREATE CONSTRAINT equip_canonical IF NOT EXISTS FOR (n:Оборудование) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT doc_canonical IF NOT EXISTS FOR (n:Документ) REQUIRE n.doc_id IS UNIQUE",
    "CREATE CONSTRAINT ore_canonical IF NOT EXISTS FOR (n:Руда_Сырье) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT plant_canonical IF NOT EXISTS FOR (n:Завод_Установка) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT flow_canonical IF NOT EXISTS FOR (n:Материальный_Поток) REQUIRE n.name IS UNIQUE",
]


def create_constraints(graph: Neo4jGraph) -> None:
    """Создаёт ограничения уникальности в Neo4j."""
    for c in CONSTRAINTS:
        graph.query(c)
    print("✅ Все ограничения схемы созданы/подтверждены.")


def load_docs_to_graph(docs: List[Dict[str, Any]], graph: Neo4jGraph) -> None:
    """
    Идемпотентная загрузка документов в граф (MERGE).
    Безопасно запускать повторно — дублей не создаёт.
    """
    for doc in docs:
        # 1. Upsert узла Документ
        graph.query(
            """
            MERGE (d:Документ {doc_id: $doc_id})
            SET d.title = $title, d.source_type = $source_type, d.updated_at = timestamp()
            """,
            doc,
        )

        # 2. Upsert сущностей
        for ent in doc["entities"]:
            label = ent["type"]
            pk = UNIQUE_KEYS[label]
            props = {**ent["props"], "mentioned_in": doc["doc_id"]}
            graph.query(
                f"""
                MERGE (n:{label} {{{pk}: $props.{pk}}})
                SET n += $props
                """,
                {"props": props},
            )

        # 3. Upsert связей
        for rel in doc["relations"]:
            src_type, src_val = rel["source"]
            tgt_type, tgt_val = rel["target"]
            src_pk = UNIQUE_KEYS[src_type]
            tgt_pk = UNIQUE_KEYS[tgt_type]
            graph.query(
                f"""
                MATCH (s:{src_type} {{{src_pk}: $src_val}})
                MATCH (t:{tgt_type} {{{tgt_pk}: $tgt_val}})
                MERGE (s)-[r:{rel['type']}]->(t)
                SET r += $props, r.source_doc = $source_doc
                """,
                {
                    "src_val": src_val,
                    "tgt_val": tgt_val,
                    "props": rel["props"],
                    "source_doc": doc["doc_id"],
                },
            )

    print(f"✅ Загружено документов: {len(docs)}. Граф обновлён инкрементально.")


def print_graph_stats(graph: Neo4jGraph) -> None:
    """Выводит статистику узлов и связей."""
    result = graph.query("MATCH (n) RETURN count(n) as total_nodes")
    print(f"Всего узлов: {result[0]['total_nodes']}")

    result = graph.query("MATCH ()-[r]->() RETURN count(r) as total_rels")
    print(f"Всего связей: {result[0]['total_rels']}")

    result = graph.query(
        "MATCH (n) RETURN labels(n)[0] as label, count(n) as count ORDER BY count DESC"
    )
    print("\nУзлы по типам:")
    for row in result:
        print(f"  {row['label']}: {row['count']}")

    result = graph.query(
        "MATCH ()-[r]->() RETURN type(r) as rel_type, count(r) as count ORDER BY count DESC"
    )
    print("\nСвязи по типам:")
    for row in result:
        print(f"  {row['rel_type']}: {row['count']}")
