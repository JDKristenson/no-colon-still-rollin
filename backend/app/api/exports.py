"""Medical report export API endpoints"""
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
import sys
from pathlib import Path
import io
from datetime import datetime
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from database import Database

router = APIRouter()


def generate_comprehensive_report(user_id: int = 1):
    """Generate comprehensive medical report with all patient data"""
    db = Database()

    # Get user info
    user = db.get_user(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get weight history
    weight_history = db.get_weight_history(user_id, limit=100)

    # Get compliance history
    compliance_history = db.get_compliance_history(user_id, days=90)

    # Get protocol foods
    foods = db.get_all_foods()

    db.close()

    return {
        'user': user,
        'weight_history': weight_history,
        'compliance_history': compliance_history,
        'foods': foods
    }


@router.get("/medical-report/excel")
def export_excel_report(user_id: int = 1):
    """
    Generate comprehensive Excel report for medical providers

    Includes:
    - Patient summary
    - Weight history with trends
    - Compliance tracking
    - Protocol foods with dosing
    """
    try:
        data = generate_comprehensive_report(user_id)
        user = data['user']

        # Create Excel writer in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:

            # Sheet 1: Patient Summary
            summary_data = {
                'Patient Name': [user['name']],
                'Cancer Type': [user['cancer_type']],
                'Current Weight (lbs)': [user['current_weight_lbs']],
                'Target Weight (lbs)': [user.get('target_weight_lbs', 'N/A')],
                'Report Generated': [datetime.now().strftime('%Y-%m-%d %H:%M')],
                'Days on Protocol': [len(data['compliance_history'])],
            }
            df_summary = pd.DataFrame(summary_data)
            df_summary.to_excel(writer, sheet_name='Patient Summary', index=False)

            # Sheet 2: Weight History
            if data['weight_history']:
                weight_data = []
                for record in data['weight_history']:
                    weight_data.append({
                        'Date': record['date'].split('T')[0] if 'T' in record['date'] else record['date'],
                        'Weight (lbs)': record['weight_lbs'],
                        'Followed Protocol': 'Yes' if record.get('followed_protocol') else 'No',
                        'Notes': record.get('notes', '')
                    })
                df_weight = pd.DataFrame(weight_data)
                df_weight.to_excel(writer, sheet_name='Weight History', index=False)

            # Sheet 3: Compliance History
            if data['compliance_history']:
                compliance_data = []
                for record in data['compliance_history']:
                    compliance_data.append({
                        'Date': record['date'].split('T')[0] if 'T' in record['date'] else record['date'],
                        'Adherence %': record['adherence_percentage'],
                        'Foods Consumed': len(record.get('foods_consumed', [])),
                        'Missed Foods': ', '.join(record.get('missed_foods', [])),
                        'Notes': record.get('notes', '')
                    })
                df_compliance = pd.DataFrame(compliance_data)
                df_compliance.to_excel(writer, sheet_name='Compliance History', index=False)

            # Sheet 4: Protocol Foods
            if data['foods']:
                foods_data = []
                for food in data['foods']:
                    foods_data.append({
                        'Food Name': food['name'],
                        'Preparation': food.get('best_preparation', 'N/A'),
                        'Max Daily Amount (g)': food.get('max_daily_amount_grams', 'N/A'),
                        'Net Carbs/100g': food.get('net_carbs_per_100g', 'N/A'),
                        'Cancer Types': ', '.join(food.get('cancer_types', [])) if food.get('cancer_types') else 'N/A',
                        'Key Mechanisms': ', '.join(food.get('mechanisms', [])[:3]) if food.get('mechanisms') else 'N/A'
                    })
                df_foods = pd.DataFrame(foods_data)
                df_foods.to_excel(writer, sheet_name='Protocol Foods', index=False)

        output.seek(0)

        filename = f"medical_report_{user['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.xlsx"

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/medical-report/csv")
def export_csv_report(user_id: int = 1, report_type: str = "weight"):
    """
    Generate CSV report for medical providers

    Parameters:
    - report_type: "weight", "compliance", or "foods"
    """
    try:
        data = generate_comprehensive_report(user_id)
        user = data['user']

        if report_type == "weight":
            if not data['weight_history']:
                raise HTTPException(status_code=404, detail="No weight history found")

            weight_data = []
            for record in data['weight_history']:
                weight_data.append({
                    'Date': record['date'].split('T')[0] if 'T' in record['date'] else record['date'],
                    'Weight (lbs)': record['weight_lbs'],
                    'Followed Protocol': 'Yes' if record.get('followed_protocol') else 'No',
                    'Notes': record.get('notes', '')
                })
            df = pd.DataFrame(weight_data)
            filename = f"weight_history_{user['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"

        elif report_type == "compliance":
            if not data['compliance_history']:
                raise HTTPException(status_code=404, detail="No compliance history found")

            compliance_data = []
            for record in data['compliance_history']:
                compliance_data.append({
                    'Date': record['date'].split('T')[0] if 'T' in record['date'] else record['date'],
                    'Adherence %': record['adherence_percentage'],
                    'Foods Consumed': len(record.get('foods_consumed', [])),
                    'Missed Foods': ', '.join(record.get('missed_foods', [])),
                    'Notes': record.get('notes', '')
                })
            df = pd.DataFrame(compliance_data)
            filename = f"compliance_history_{user['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"

        elif report_type == "foods":
            if not data['foods']:
                raise HTTPException(status_code=404, detail="No foods found")

            foods_data = []
            for food in data['foods']:
                foods_data.append({
                    'Food Name': food['name'],
                    'Preparation': food.get('best_preparation', 'N/A'),
                    'Max Daily Amount (g)': food.get('max_daily_amount_grams', 'N/A'),
                    'Net Carbs/100g': food.get('net_carbs_per_100g', 'N/A'),
                    'Cancer Types': ', '.join(food.get('cancer_types', [])) if food.get('cancer_types') else 'N/A'
                })
            df = pd.DataFrame(foods_data)
            filename = f"protocol_foods_{user['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.csv"

        else:
            raise HTTPException(status_code=400, detail="Invalid report_type. Must be 'weight', 'compliance', or 'foods'")

        # Convert DataFrame to CSV
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        return StreamingResponse(
            iter([csv_buffer.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary-report")
def get_summary_report(user_id: int = 1):
    """Get a JSON summary report for display"""
    try:
        data = generate_comprehensive_report(user_id)
        user = data['user']

        # Calculate statistics
        weight_history = data['weight_history']
        starting_weight = weight_history[-1]['weight_lbs'] if weight_history else user['current_weight_lbs']
        current_weight = user['current_weight_lbs']
        weight_change = current_weight - starting_weight

        compliance_history = data['compliance_history']
        avg_adherence = sum(r['adherence_percentage'] for r in compliance_history) / len(compliance_history) if compliance_history else 0

        # Current streak
        current_streak = 0
        for record in compliance_history:
            if record['adherence_percentage'] >= 80:
                current_streak += 1
            else:
                break

        return {
            'patient_name': user['name'],
            'cancer_type': user['cancer_type'],
            'report_date': datetime.now().strftime('%Y-%m-%d'),
            'weight_stats': {
                'current_weight_lbs': current_weight,
                'starting_weight_lbs': starting_weight,
                'weight_change_lbs': round(weight_change, 1),
                'total_measurements': len(weight_history)
            },
            'compliance_stats': {
                'average_adherence': round(avg_adherence, 1),
                'current_streak_days': current_streak,
                'total_days_tracked': len(compliance_history)
            },
            'protocol_summary': {
                'total_foods': len(data['foods']),
                'food_names': [f['name'] for f in data['foods']]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
