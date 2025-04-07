from typing import List, Dict, Any, Optional, Tuple
from base_dao import BaseDAO

class CharacterDAO(BaseDAO):
    def create(self, name: str, role: str, description: str = None, motivation: str = None) -> int:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                INSERT INTO `Character` (name, role, description, motivation)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (name, role, description, motivation))
                connection.commit()
                return cursor.lastrowid
        except Exception as e:
            connection.rollback()
            raise e
    
    def get_by_id(self, character_id: int) -> Optional[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Character` WHERE id = %s"
                cursor.execute(sql, (character_id,))
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def get_by_name(self, name: str) -> Optional[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Character` WHERE name = %s"
                cursor.execute(sql, (name,))
                return cursor.fetchone()
        except Exception as e:
            raise e
    
    def get_all(self) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `Character`"
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
    
    def update(self, character_id: int, name: str = None, role: str = None, 
               description: str = None, motivation: str = None) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                updates = []
                params = []
                
                if name is not None:
                    updates.append("name = %s")
                    params.append(name)
                if role is not None:
                    updates.append("role = %s")
                    params.append(role)
                if description is not None:
                    updates.append("description = %s")
                    params.append(description)
                if motivation is not None:
                    updates.append("motivation = %s")
                    params.append(motivation)
                
                if not updates:
                    return False
                
                sql = f"UPDATE `Character` SET {', '.join(updates)} WHERE id = %s"
                params.append(character_id)
                
                cursor.execute(sql, params)
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e
    
    def delete(self, character_id: int) -> bool:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = "DELETE FROM `Character` WHERE id = %s"
                cursor.execute(sql, (character_id,))
                connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            connection.rollback()
            raise e 
        
    def get_all_with_events(self) -> List[Dict]:
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT c.*, e.id as event_id, e.title as event_title
                FROM `Character` c
                LEFT JOIN `Event` e ON c.id = e.character_id
                """
                cursor.execute(sql)
                return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            connection.close()