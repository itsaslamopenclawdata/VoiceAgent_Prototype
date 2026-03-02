"""
RepCon Voice Agent - Google Sheets Integration Service
"""
import asyncio
from typing import List, Dict, Optional
from datetime import datetime
import httpx


class GoogleSheetsService:
    """Google Sheets integration for course data sync"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
    
    def __init__(self, service_account_json: str = None, spreadsheet_id: str = None):
        self.service_account_json = service_account_json
        self.spreadsheet_id = spreadsheet_id
        self._credentials = None
        self._service = None
    
    async def initialize(self):
        """Initialize Google Sheets client"""
        if not self.service_account_json:
            print("Warning: Google Sheets credentials not configured")
            return
        
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build
            
            # Parse credentials
            import json
            credentials_info = json.loads(self.service_account_json)
            
            # Create credentials
            self._credentials = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=self.SCOPES
            )
            
            # Build service
            self._service = build('sheets', 'v4', credentials=self._credentials)
            
            print("Google Sheets service initialized")
            
        except Exception as e:
            print(f"Google Sheets initialization error: {e}")
    
    async def sync_courses(
        self,
        spreadsheet_id: str,
        institute_id: int,
        db_session
    ) -> Dict:
        """
        Sync courses from Google Sheets
        
        Args:
            spreadsheet_id: Google Sheets ID
            institute_id: Institute ID in database
            db_session: Database session
            
        Returns:
            Dict with sync results
        """
        if not self._service:
            await self.initialize()
        
        if not self._service:
            return {
                "success": False,
                "message": "Google Sheets not configured",
                "added": 0,
                "updated": 0,
                "errors": ["Service not initialized"]
            }
        
        try:
            # Get values from sheet
            result = self._service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range='Courses!A:H'  # Adjust based on actual sheet structure
            ).execute()
            
            values = result.get('values', [])
            
            if not values:
                return {
                    "success": False,
                    "message": "No data found in sheet",
                    "added": 0,
                    "updated": 0
                }
            
            # First row is headers
            headers = values[0] if values else []
            data_rows = values[1:] if len(values) > 1 else []
            
            # Map columns
            column_map = self._map_columns(headers)
            
            # Process rows
            added = 0
            updated = 0
            errors = []
            
            for row_idx, row in enumerate(data_rows):
                try:
                    course_data = self._map_row_to_course(row, column_map, institute_id)
                    
                    if course_data:
                        # Check if course exists
                        from sqlalchemy import select
                        from app.models.models import Course
                        
                        result = await db_session.execute(
                            select(Course).where(
                                Course.institute_id == institute_id,
                                Course.course_code == course_data.get('course_code')
                            )
                        )
                        existing = result.scalar_one_or_none()
                        
                        if existing:
                            # Update
                            for key, value in course_data.items():
                                setattr(existing, key, value)
                            updated += 1
                        else:
                            # Create new
                            course = Course(**course_data)
                            db_session.add(course)
                            added += 1
                            
                except Exception as e:
                    errors.append(f"Row {row_idx + 2}: {str(e)}")
            
            # Commit changes
            await db_session.commit()
            
            return {
                "success": True,
                "message": f"Synced {added + updated} courses",
                "added": added,
                "updated": updated,
                "errors": errors
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Sync failed: {str(e)}",
                "added": 0,
                "updated": 0,
                "errors": [str(e)]
            }
    
    def _map_columns(self, headers: List[str]) -> Dict[str, int]:
        """Map header names to column indices"""
        header_map = {}
        
        for idx, header in enumerate(headers):
            header_lower = header.lower().strip()
            
            if header_lower in ['course name', 'name', 'course']:
                header_map['course_name'] = idx
            elif header_lower in ['course code', 'code']:
                header_map['course_code'] = idx
            elif header_lower in ['description', 'desc']:
                header_map['description'] = idx
            elif header_lower in ['duration', 'time']:
                header_map['duration'] = idx
            elif header_lower in ['fee', 'price', 'cost']:
                header_map['fee'] = idx
            elif header_lower in ['job roles', 'careers', 'roles']:
                header_map['job_roles'] = idx
            ['mode', ' elif header_lower intype']:
                header_map['mode'] = idx
            elif header_lower in ['eligibility', 'criteria']:
                header_map['eligibility'] = idx
        
        return header_map
    
    def _map_row_to_course(
        self,
        row: List[str],
        column_map: Dict[str, int],
        institute_id: int
    ) -> Optional[Dict]:
        """Map a row to course data"""
        if not row or len(row) < 4:
            return None
        
        course_data = {
            "institute_id": institute_id,
            "is_active": True,
            "source_id": self.spreadsheet_id,
            "source_updated": datetime.utcnow()
        }
        
        # Course name (required)
        course_name_idx = column_map.get('course_name', 0)
        if course_name_idx < len(row):
            course_data['course_name'] = row[course_name_idx]
        else:
            return None
        
        # Course code
        course_code_idx = column_map.get('course_code')
        if course_code_idx and course_code_idx < len(row):
            course_data['course_code'] = row[course_code_idx]
        
        # Description
        desc_idx = column_map.get('description')
        if desc_idx and desc_idx < len(row):
            course_data['description'] = row[desc_idx]
        
        # Duration (required)
        duration_idx = column_map.get('duration', 1)
        if duration_idx < len(row):
            course_data['duration'] = row[duration_idx]
        else:
            course_data['duration'] = "3 months"
        
        # Fee (required)
        fee_idx = column_map.get('fee', 2)
        if fee_idx < len(row):
            try:
                fee_str = row[fee_idx].replace('₹', '').replace(',', '').strip()
                course_data['fee'] = float(fee_str)
            except:
                course_data['fee'] = 0
        else:
            course_data['fee'] = 0
        
        # Job roles
        job_roles_idx = column_map.get('job_roles')
        if job_roles_idx and job_roles_idx < len(row):
            roles = [r.strip() for r in row[job_roles_idx].split(',')]
            course_data['job_roles'] = roles
        
        # Mode
        mode_idx = column_map.get('mode')
        if mode_idx and mode_idx < len(row):
            course_data['mode'] = row[mode_idx].lower()
        else:
            course_data['mode'] = 'online'
        
        # Eligibility
        elig_idx = column_map.get('eligibility')
        if elig_idx and elig_idx < len(row):
            course_data['eligibility'] = row[elig_idx]
        
        return course_data
    
    async def get_sheet_data(
        self,
        spreadsheet_id: str,
        range: str = 'A1:Z100'
    ) -> List[List[str]]:
        """Get raw data from a sheet range"""
        if not self._service:
            await self.initialize()
        
        if not self._service:
            return []
        
        try:
            result = self._service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range
            ).execute()
            
            return result.get('values', [])
            
        except Exception as e:
            print(f"Error getting sheet data: {e}")
            return []


# Singleton instance
google_sheets_service = GoogleSheetsService()
