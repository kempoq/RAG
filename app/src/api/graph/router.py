from fastapi import APIRouter

from app.src.api.graph.dependencies import GraphRagServiceDep
from app.src.api.graph.schemas import ChatRequest, ChatResponse

graph_router = APIRouter(prefix="/graph", tags=["graph_rag"])


@graph_router.get("/store/stats")
def get_stats(graph_rag_service: GraphRagServiceDep):
    """Получение статистики по графу"""

    graph_stats = graph_rag_service.get_stats()

    return graph_stats


@graph_router.get("/store/schema")
def get_graph_schema(graph_rag_service: GraphRagServiceDep):
    """Получение схемы графа"""

    graph_schema = graph_rag_service.get_graph_schema()

    return {"schema": graph_schema}


@graph_router.post("/chat", response_model=ChatResponse)
def chat(
    graph_rag_service: GraphRagServiceDep, request_data: ChatRequest
) -> ChatResponse:
    """Запрос к LLM (графовый RAG)"""

    # response = graph_rag_service.chat(query=request_data.query)
    response = {
        "user_query": "Что используется в технологическом процессе?",
        "answer": "На основе представленных данных можно сделать вывод о том, что в технологических процессах используются различные вещества и реагенты:\n\n1. **Кислоты**: HNO3, H2SO4, NaClO3, HCl, H2SO4.\n2. **Щелочи и основания**: Na2CO3, Ca(OH)2, NH4OH, MgO, FeSO4, NaCN.\n3. **Окислители и восстановители**: O2, SO2, NaCN, Zn, Fe (металлическое).\n4. **Экстрагенты и комплексоны**: D2EHPA, PC-88A, Alamin-336, ЭДТА.\n5. **Депрессанты и осадители**: Na2S, Na2CO3, MgO.\n6. **Особые вещества**: Цианид, угольная пыль, аммиак, аммонийные соли.\n\nЭти вещества играют ключевую роль в различных технологических процессах, таких как десорбция, диафрагменный электролиз, жидкостная экстракция, ионная хроматография, кислотное выщелачивание, кучное выщелачивание, жиг в кипящем слое, осаждение сульфидов металлов, предварительное цианирование, реэкстракция, содовая переработка, сольвентная экстракция, сорбция из пульпы, цементация, химическое осаждение и другие процессы.",
        "cypher_query": "MATCH (tp:Технологический_Процесс)-[:ИСПОЛЬЗУЕТ*]->(n)\nWITH tp, COLLECT(n) AS elements\nRETURN tp.canonical_name AS Процесс, elements\nORDER BY tp.canonical_name",
        "graph_db_info": [
            {
                "Процесс": "Десорбция",
                "elements": [
                    {
                        "formula_or_name": "HNO3",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_002",
                        "class": "acid",
                    }
                ],
            },
            {
                "Процесс": "Десорбция индия",
                "elements": [
                    {
                        "formula_or_name": "H2SO4",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_006",
                        "class": "acid",
                    }
                ],
            },
            {
                "Процесс": "Диафрагменный электролиз хлоридов",
                "elements": [
                    {
                        "formula_or_name": "NaCl",
                        "mentioned_in": "DOC_030",
                        "class": "electrolyte",
                    }
                ],
            },
            {
                "Процесс": "Жидкостная экстракция",
                "elements": [
                    {
                        "formula_or_name": "Аламин-336",
                        "hazard_class": "3",
                        "mentioned_in": "DOC_004",
                        "class": "extractant",
                    },
                    {
                        "formula_or_name": "Керосин",
                        "hazard_class": "3",
                        "mentioned_in": "DOC_004",
                        "class": "solvent",
                    },
                ],
            },
            {
                "Процесс": "Извлечение ванадия",
                "elements": [
                    {
                        "formula_or_name": "(NH4)2CO3",
                        "hazard_class": "4",
                        "mentioned_in": "DOC_010",
                        "class": "salt",
                    }
                ],
            },
            {
                "Процесс": "Извлечение молибдена",
                "elements": [
                    {
                        "formula_or_name": "Na2S",
                        "hazard_class": "3",
                        "mentioned_in": "DOC_010",
                        "class": "reductant",
                    },
                    {
                        "formula_or_name": "Ca(OH)2",
                        "hazard_class": "3",
                        "mentioned_in": "DOC_010",
                        "class": "base",
                    },
                ],
            },
            {
                "Процесс": "Ионный обмен",
                "elements": [
                    {
                        "formula_or_name": "Анионит АВ-17",
                        "hazard_class": "3",
                        "mentioned_in": "DOC_002",
                        "class": "extractant",
                    }
                ],
            },
            {
                "Процесс": "Ионообменная хроматография РЗЭ",
                "elements": [
                    {
                        "formula_or_name": "Комплексон III (ЭДТА)",
                        "mentioned_in": "DOC_018",
                        "class": "complexant",
                    },
                    {
                        "formula_or_name": "NH4Cl",
                        "mentioned_in": "DOC_018",
                        "class": "eluent",
                    },
                ],
            },
            {
                "Процесс": "Кислотное выщелачивание",
                "elements": [
                    {
                        "formula_or_name": "H2SO4",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_006",
                        "class": "acid",
                    },
                    {
                        "formula_or_name": "NaClO3",
                        "mentioned_in": "DOC_001",
                        "class": "oxidant",
                    },
                ],
            },
            {
                "Процесс": "Кислотное выщелачивание РЗЭ-магнитов",
                "elements": [
                    {
                        "formula_or_name": "HCl",
                        "mentioned_in": "DOC_016",
                        "class": "acid",
                    }
                ],
            },
            {
                "Процесс": "Кислотное выщелачивание огарка",
                "elements": [
                    {
                        "formula_or_name": "H2SO4",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_006",
                        "class": "acid",
                    }
                ],
            },
            {
                "Процесс": "Коллективная флотация",
                "elements": [
                    {
                        "formula_or_name": "Цианид",
                        "mentioned_in": "DOC_011",
                        "class": "depressant",
                    },
                    {
                        "formula_or_name": "Цинковый купорос",
                        "mentioned_in": "DOC_011",
                        "class": "depressant",
                    },
                ],
            },
            {
                "Процесс": "Кучное выщелачивание",
                "elements": [
                    {
                        "formula_or_name": "H2SO4",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_006",
                        "class": "acid",
                    }
                ],
            },
            {
                "Процесс": "Обжиг в кипящем слое",
                "elements": [
                    {
                        "formula_or_name": "O2",
                        "mentioned_in": "DOC_017",
                        "class": "oxidant",
                    }
                ],
            },
            {
                "Процесс": "Осаждение сульфидов металлов",
                "elements": [
                    {
                        "phase_state": "aqueous",
                        "role_in_reaction": "sulfidant",
                        "formula": "Na2S",
                        "mentioned_in": "DOC_031",
                    }
                ],
            },
            {
                "Процесс": "Подземное выщелачивание меди",
                "elements": [
                    {
                        "formula_or_name": "H2SO4",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_006",
                        "class": "acid",
                    },
                    {
                        "formula_or_name": "SO2",
                        "mentioned_in": "DOC_020",
                        "class": "reductant",
                    },
                ],
            },
            {
                "Процесс": "Предварительное цианирование в пачуках",
                "elements": [
                    {
                        "formula_or_name": "Ca(OH)2",
                        "hazard_class": "3",
                        "mentioned_in": "DOC_010",
                        "class": "base",
                    },
                    {
                        "formula_or_name": "NaCN",
                        "mentioned_in": "DOC_021",
                        "class": "complexant",
                    },
                ],
            },
            {
                "Процесс": "Реэкстракция",
                "elements": [
                    {
                        "formula_or_name": "(NH4)2SO4",
                        "hazard_class": "4",
                        "mentioned_in": "DOC_004",
                        "class": "salt",
                    }
                ],
            },
            {
                "Процесс": "Содовая переработка целестина",
                "elements": [
                    {
                        "formula_or_name": "Na2CO3",
                        "hazard_class": "4",
                        "mentioned_in": "DOC_005",
                        "class": "base",
                    }
                ],
            },
            {
                "Процесс": "Содовое автоклавное выщелачивание",
                "elements": [
                    {
                        "formula_or_name": "Na2CO3",
                        "hazard_class": "4",
                        "mentioned_in": "DOC_005",
                        "class": "base",
                    }
                ],
            },
            {
                "Процесс": "Сольвентная экстракция РЗЭ",
                "elements": [
                    {
                        "formula_or_name": "D2EHPA",
                        "mentioned_in": "DOC_016",
                        "class": "extractant",
                    },
                    {
                        "formula_or_name": "PC-88A",
                        "mentioned_in": "DOC_016",
                        "class": "extractant",
                    },
                ],
            },
            {
                "Процесс": "Сорбция из пульпы",
                "elements": [
                    {
                        "formula_or_name": "MgO",
                        "hazard_class": "4",
                        "mentioned_in": "DOC_009",
                        "class": "base",
                    },
                    {
                        "formula_or_name": "FeSO4",
                        "hazard_class": "4",
                        "mentioned_in": "DOC_009",
                        "class": "reductant",
                    },
                ],
            },
            {
                "Процесс": "Фьюмингование",
                "elements": [
                    {
                        "formula_or_name": "Угольная пыль",
                        "mentioned_in": "DOC_013",
                        "class": "reductant",
                    }
                ],
            },
            {
                "Процесс": "Химическое осаждение",
                "elements": [
                    {
                        "formula_or_name": "NH4OH",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_005",
                        "class": "base",
                    },
                    {
                        "formula_or_name": "MgO",
                        "hazard_class": "4",
                        "mentioned_in": "DOC_009",
                        "class": "base",
                    },
                    {
                        "formula_or_name": "NaOH",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_008",
                        "class": "base",
                    },
                    {
                        "formula_or_name": "H2O2",
                        "hazard_class": "2",
                        "mentioned_in": "DOC_008",
                        "class": "oxidant",
                    },
                ],
            },
            {
                "Процесс": "Цементация золота цинком",
                "elements": [
                    {
                        "formula_or_name": "Zn",
                        "mentioned_in": "DOC_017",
                        "class": "cementator",
                    }
                ],
            },
            {
                "Процесс": "Цементация меди железом",
                "elements": [
                    {
                        "formula_or_name": "Fe (металлическое)",
                        "mentioned_in": "DOC_019",
                        "class": "cementator",
                    }
                ],
            },
            {
                "Процесс": "Цианирование золота",
                "elements": [
                    {
                        "formula_or_name": "O2",
                        "mentioned_in": "DOC_017",
                        "class": "oxidant",
                    },
                    {
                        "formula_or_name": "NaCN",
                        "mentioned_in": "DOC_021",
                        "class": "complexant",
                    },
                ],
            },
        ],
        "token_usage": 4561,
        "vector_db_info": [
            "## ПРИМЕНЕНИЕ АВТОКЛАВНЫХ ПРОЦЕССОВ В ГИДРОМЕТАЛЛУРГИИ¹\n\n### ВВЕДЕНИЕ\n\nПотребность современной техники во всех химических элементах периодической системы обусловливает необходимость комплексного, и в то же время экономичного, извлечения ценных составляющих природного сырья. Одним из путей решения этой задачи является применение повышенных температур и давлений в гидрометаллургии.\n\nНагрев растворов и пульп в автоклавах создает возможность проведения разнообразных гидрометаллургических процессов при темпера-\n\n¹ Автор канд. техн. наук С. И. Соболь, рецензенты канд. техн. наук Г. Н. Доброхотов и канд. техн. наук Н. Н. Масленицкий, редакторы проф. докт. техн. наук Н. С. Грейвер и канд. техн. наук В. Н. Никифоров.\n\n============================================================\n[СТРАНИЦА 232 (часть 2, локальная 82)]\n============================================================\n\nПрименение автоклавных процессов в гидрометаллургии",
            "Во многих случаях практики отдельные элементы могут быть заменены другими, но, наряду с этим, каждому из них присущи какие-то свои специфические свойства, обусловливающие его незаменимость. И если уже теперь в технике применяется большая часть элементов, то общая тенденция к использованию всей их ассоциации стала значением времени. Это в равной мере относится и к металлам, и к неметаллам¹. Уместно напомнить, что из числа неметаллов металлургическая промышленность производит серу, мышьяк, селен, теллур и некоторые их соединения, кремний, фосфор, бор и их сплавы; в процессе производства сжигается твердое, жидкое и газообразное топливо; используется воздух и раздельно кислород, водород, азот, гелий и аргон; применяются галогены — фтор, хлор, бром, йод и их соединения.",
            "Весьма большое влияние на ход металлургических процессов оказывают тепловые и физические свойства материалов и продуктов переработки. Наиболее важными свойствами являются: температура плавления, вязкость, удельный вес, теплоемкость, теплопотребление, электро- и теплопроводность. К сожалению, имеющиеся в настоящее время экспериментальные и теоретические данные по термодинамике, тепловым и физическим свойствам материалов применительно к процессам цветной металлургии недостаточны и их практическое использование для формирования теории и расчета печей ограничено.\n\nКак показано ниже, на основании закономерностей протекания ме-\n\n============================================================\n[СТРАНИЦА 514 (часть 4, локальная 64)]\n============================================================\n\nОсновы теории металлургических печей",
        ],
    }

    return response
