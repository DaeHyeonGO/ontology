from typing import List, Dict, Any, Optional, Tuple
from base_dao import BaseDAO

class EventDAO(BaseDAO):
    def create(self, title: str, description: str, importance: int = 1) -> int:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO `Event` (title, description, importance)
                VALUES (%s, %s, %s)
                """
                cursor.execute(sql, (title, description, importance))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_by_id(self, event_id: int) -> Optional[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Event` WHERE id = %s"
                cursor.execute(sql, (event_id,))
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def get_all(self) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Event`"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def update(self, event_id: int, title: str = None, description: str = None, importance: int = None) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                updates = []
                params = []
                
                if title is not None:
                    updates.append("title = %s")
                    params.append(title)
                if description is not None:
                    updates.append("description = %s")
                    params.append(description)
                if importance is not None:
                    updates.append("importance = %s")
                    params.append(importance)
                
                if not updates:
                    return False
                
                sql = f"UPDATE `Event` SET {', '.join(updates)} WHERE id = %s"
                params.append(event_id)
                
                cursor.execute(sql, params)
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def delete(self, event_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Event` WHERE id = %s"
                cursor.execute(sql, (event_id,))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def add_character(self, event_id: int, character_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO Event_Character (event_id, character_id)
                VALUES (%s, %s)
                """
                cursor.execute(sql, (event_id, character_id))
                connection.commit()
                return True
        except Exception as e:
            connection.rollback()
            raise e
    
    def remove_character(self, event_id: int, character_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                DELETE FROM Event_Character 
                WHERE event_id = %s AND character_id = %s
                """
                cursor.execute(sql, (event_id, character_id))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_characters(self, event_id: int) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT c.* FROM `Character` c
                JOIN Event_Character ec ON c.id = ec.character_id
                WHERE ec.event_id = %s
                """
                cursor.execute(sql, (event_id,))
                return cursor.fetchall()
        except Exception as e:
            raise e 