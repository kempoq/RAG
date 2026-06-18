from app.src.core.database.graph_database import get_graph

if __name__ == "__main__":
    g = get_graph()
    query = 'MATCH (tp:Технологический_Процесс)-[:ИСПОЛЬЗУЕТ]->(hr:Химический_Реагент),(tp)-[:РАЗМЕЩАЕТСЯ_В]->(ob:Оборудование) WHERE tp.canonical_name CONTAINS "выщелачивание" AND hr.formula_or_name CONTAINS "Сода" RETURN ob.name AS Оборудование, hr.formula_or_name AS Реагент, tp.stage_type AS Тип_процесса, tp.description AS Описание_процесса ORDER BY ob.name'
    res = g.query(query=query)
    print(res)
