"""
Compliance tracking for No Colon, Still Rollin'
Simple interface for Jesse to track what he actually ate
"""
import argparse
from datetime import datetime, date
from typing import List, Dict

from database import Database


class ComplianceTracker:
    """Track daily compliance with protocol"""

    def __init__(self):
        self.db = Database()

    def record_weight(self, user_name: str, weight_lbs: float,
                     followed_protocol: bool = True, notes: str = ""):
        """Record weekly weight (Monday morning protocol)"""

        user = self.db.get_user(name=user_name)
        if not user:
            raise ValueError(f"User '{user_name}' not found")

        # Add weight record
        self.db.add_weight_record(
            user_id=user['id'],
            weight_lbs=weight_lbs,
            followed_protocol=followed_protocol,
            notes=notes
        )

        print(f"\n✅ Weight recorded: {weight_lbs} lbs")
        print(f"   Protocol followed: {'Yes' if followed_protocol else 'No'}")
        if notes:
            print(f"   Notes: {notes}")

    def quick_compliance_check(self, user_name: str = "Jesse Mills"):
        """Quick daily check-in"""

        user = self.db.get_user(name=user_name)
        if not user:
            raise ValueError(f"User '{user_name}' not found")

        today = date.today().isoformat()

        # Get today's protocol
        protocol = self.db.get_protocol_for_date(user['id'], today)

        if not protocol:
            print(f"\n⚠️  No protocol found for today ({today})")
            print("   Generate one with: python src/protocol_generator.py")
            return

        print(f"\n{'='*60}")
        print(f"Daily Compliance Check - {today}")
        print(f"{'='*60}\n")

        foods_consumed = []
        missed_foods = []
        total_consumed = 0
        total_expected = len(protocol['foods'])

        for food_item in protocol['foods']:
            food_name = food_item['name']
            expected_amount = food_item['amount_grams']

            print(f"\n{food_name}:")
            print(f"  Expected: {expected_amount}g ({food_item['servings_per_day']}x {food_item['grams_per_serving']}g)")
            print(f"  Timing: {food_item['timing_notes']}")

            response = input(f"  Did you eat this? (y/n/[amount in grams]): ").strip().lower()

            if response in ['y', 'yes']:
                foods_consumed.append({
                    "food": food_name,
                    "expected_grams": expected_amount,
                    "actual_grams": expected_amount,
                    "percentage": 100
                })
                total_consumed += 1
                print(f"  ✅ Full dose consumed")

            elif response in ['n', 'no']:
                missed_foods.append(food_name)
                print(f"  ❌ Missed")

            elif response.replace('.', '').isdigit():
                actual_amount = float(response)
                percentage = (actual_amount / expected_amount) * 100
                foods_consumed.append({
                    "food": food_name,
                    "expected_grams": expected_amount,
                    "actual_grams": actual_amount,
                    "percentage": round(percentage, 1)
                })
                if percentage >= 80:
                    total_consumed += 1
                    print(f"  ✅ {percentage:.0f}% consumed")
                else:
                    print(f"  ⚠️  Only {percentage:.0f}% consumed")

        # Calculate adherence
        adherence = (total_consumed / total_expected) * 100 if total_expected > 0 else 0

        print(f"\n{'='*60}")
        print(f"SUMMARY:")
        print(f"{'='*60}")
        print(f"Foods consumed: {total_consumed}/{total_expected}")
        print(f"Adherence: {adherence:.0f}%")

        if missed_foods:
            print(f"\n⚠️  Missed: {', '.join(missed_foods)}")

        # Ask for notes
        notes = input("\nAny notes about today (side effects, challenges, etc.)? ").strip()

        # Save compliance record
        compliance_data = {
            "user_id": user['id'],
            "protocol_id": protocol['id'],
            "date": today,
            "foods_consumed": foods_consumed,
            "adherence_percentage": round(adherence, 1),
            "missed_foods": missed_foods,
            "notes": notes,
        }

        self.db.record_compliance(compliance_data)

        print(f"\n✅ Compliance recorded for {today}")

        # Give feedback
        if adherence >= 90:
            print("\n🎉 Excellent adherence! Keep it up!")
        elif adherence >= 70:
            print("\n👍 Good job! Try to hit all foods tomorrow.")
        else:
            print("\n💪 Let's aim higher tomorrow. You've got this!")

    def show_compliance_history(self, user_name: str, days: int = 7):
        """Show recent compliance history"""

        user = self.db.get_user(name=user_name)
        if not user:
            raise ValueError(f"User '{user_name}' not found")

        records = self.db.get_compliance_history(user['id'], days)

        if not records:
            print(f"\n⚠️  No compliance records found")
            return

        print(f"\n{'='*60}")
        print(f"Compliance History - Last {days} Days")
        print(f"{'='*60}\n")

        for record in reversed(records):  # Show oldest first
            date_str = record['date']
            adherence = record['adherence_percentage']

            # Visual indicator
            if adherence >= 90:
                indicator = "🟢"
            elif adherence >= 70:
                indicator = "🟡"
            else:
                indicator = "🔴"

            print(f"{indicator} {date_str}: {adherence}% adherence")

            if record['missed_foods']:
                print(f"   Missed: {', '.join(record['missed_foods'])}")

            if record['notes']:
                print(f"   Notes: {record['notes']}")

            print()

        # Calculate average
        avg_adherence = sum(r['adherence_percentage'] for r in records) / len(records)
        print(f"Average adherence: {avg_adherence:.1f}%")

        # Count streak
        streak = 0
        for record in records:
            if record['adherence_percentage'] >= 80:
                streak += 1
            else:
                break

        if streak > 0:
            print(f"Current streak: {streak} days ≥80% adherence 🔥")


def main():
    """Command line interface"""
    parser = argparse.ArgumentParser(
        description="Track compliance with anti-cancer protocol"
    )
    parser.add_argument(
        "--user",
        default="Jesse Mills",
        help="User name (default: Jesse Mills)"
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Weight command
    weight_parser = subparsers.add_parser('weight', help='Record weekly weight')
    weight_parser.add_argument('weight', type=float, help='Weight in pounds')
    weight_parser.add_argument('--notes', default='', help='Optional notes')
    weight_parser.add_argument('--no-protocol', action='store_true',
                              help='Flag if weighing protocol was not followed')

    # Check command
    subparsers.add_parser('check', help='Daily compliance check')

    # History command
    history_parser = subparsers.add_parser('history', help='Show compliance history')
    history_parser.add_argument('--days', type=int, default=7, help='Number of days (default: 7)')

    args = parser.parse_args()

    tracker = ComplianceTracker()

    try:
        if args.command == 'weight':
            tracker.record_weight(
                user_name=args.user,
                weight_lbs=args.weight,
                followed_protocol=not args.no_protocol,
                notes=args.notes
            )

        elif args.command == 'check':
            tracker.quick_compliance_check(user_name=args.user)

        elif args.command == 'history':
            tracker.show_compliance_history(user_name=args.user, days=args.days)

        else:
            # Default: quick check
            tracker.quick_compliance_check(user_name=args.user)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
