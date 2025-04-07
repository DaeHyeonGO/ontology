from typing import List, Dict, Any, Optional, Tuple
from base_dao import BaseDAO

class PlotPointDAO(BaseDAO):
    def create(self, event_id: int, timing: str, emotional_impact: str = None) -> int:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO PlotPoint (event_id, timing, emotional_impact)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (event_id, timing, emotional_impact))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_by_id(self, plotpoint_id: int) -> Optional[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM PlotPoint WHERE id = %s"
                cursor.execute(sql, (plotpoint_id,))
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def get_all(self) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM PlotPoint"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def get_by_timing(self, timing: str) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM PlotPoint WHERE timing = %s"
                cursor.execute(sql, (timing,))
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def update(self, plotpoint_id: int, event_id: int = None, timing: str = None, 
               emotional_impact: str = None) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                updates = []
                params = []
                
                if event_id is not None:
                    updates.append("event_id = %s")
                    params.append(event_id)
                if timing is not None:
                    updates.append("timing = %s")
                    params.append(timing)
                if emotional_impact is not None:
                    updates.append("emotional_impact = %s")
                    params.append(emotional_impact)
                
                if not updates:
                    return False
                
                sql = f"UPDATE PlotPoint SET {', '.join(updates)} WHERE id = %s"
                params.append(plotpoint_id)
                
                cursor.execute(sql, params)
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def delete(self, plotpoint_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM PlotPoint WHERE id = %s"
                cursor.execute(sql, (plotpoint_id,))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def add_consequence(self, plotpoint_id: int, consequence: str) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO PlotPoint_Consequence (plotpoint_id, consequence)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (plotpoint_id, consequence))
                connection.commit()
                return True
        except Exception as e:
            connection.rollback()
            raise e
    
    def remove_consequence(self, plotpoint_id: int, consequence: str) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM PlotPoint_Consequence 
                WHERE plotpoint_id = %s AND consequence = %s
                """
                cursor.execute(sql, (plotpoint_id, consequence))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_consequences(self, plotpoint_id: int) -> List[str]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT consequence FROM PlotPoint_Consequence
                WHERE plotpoint_id = %s
                """
                cursor.execute(sql, (plotpoint_id,))
                results = cursor.fetchall()
                return [result['consequence'] for result in results]
        except Exception as e:
            raise e 