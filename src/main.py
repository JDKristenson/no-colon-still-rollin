#!/usr/bin/env python3
"""
No Colon, Still Rollin' - Main CLI
Simple interface for Jesse to use the system
"""
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from init_database import main as init_db
from pubmed_fetcher import PubMedFetcher
from protocol_generator import ProtocolGenerator
from track_compliance import ComplianceTracker
from database import Database


def setup():
    """Initial setup"""
    print("\n🚀 Setting up No Colon, Still Rollin'...\n")

    # Initialize database
    print("Step 1: Initializing database...")
    init_db()

    print("\nSetup complete! ✅")
    print("\nNext steps:")
    print("  1. Update research: python src/main.py update-research")
    print("  2. Generate protocol: python src/main.py protocol")
    print("  3. Track daily: python src/main.py track")


def update_research(max_per_search: int = 20):
    """Update research database from PubMed"""
    print("\n🔬 Updating research from PubMed...\n")

    try:
        fetcher = PubMedFetcher()
        fetcher.update_research_database(max_per_search=max_per_search)

        print("\n📊 Research Summary:")
        summary = fetcher.get_research_summary()
        print(f"  Total studies: {summary['total_studies']}")
        print(f"  Top foods:")
        for food, count in list(summary['top_foods'].items())[:5]:
            print(f"    - {food}: {count} studies")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "Biopython" in str(e):
            print("\n💡 Install biopython: pip install biopython")


def generate_protocol(user: str = "Jesse Mills", weight: float = None):
    """Generate daily protocol"""
    print(f"\n📋 Generating protocol for {user}...\n")

    try:
        generator = ProtocolGenerator()
        protocol = generator.generate_daily_protocol(
            user_name=user,
            weight_lbs=weight
        )
        generator.print_protocol(protocol)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "not found" in str(e):
            print("\n💡 Run setup first: python src/main.py setup")


def track_compliance(user: str = "Jesse Mills"):
    """Track daily compliance"""
    try:
        tracker = ComplianceTracker()
        tracker.quick_compliance_check(user_name=user)
    except Exception as e:
        print(f"\n❌ Error: {e}")


def record_weight(user: str, weight: float):
    """Record weekly weight"""
    try:
        tracker = ComplianceTracker()
        tracker.record_weight(user_name=user, weight_lbs=weight)
    except Exception as e:
        print(f"\n❌ Error: {e}")


def show_history(user: str, days: int = 7):
    """Show compliance history"""
    try:
        tracker = ComplianceTracker()
        tracker.show_compliance_history(user_name=user, days=days)
    except Exception as e:
        print(f"\n❌ Error: {e}")


def show_status(user: str = "Jesse Mills"):
    """Show current status"""
    print(f"\n{'='*60}")
    print(f"Status for {user}")
    print(f"{'='*60}\n")

    try:
        db = Database()

        # User info
        user_data = db.get_user(name=user)
        if not user_data:
            print(f"❌ User '{user}' not found. Run setup first.")
            return

        print(f"Current weight: {user_data['current_weight_lbs']} lbs")
        if user_data.get('target_weight_lbs'):
            print(f"Target weight: {user_data['target_weight_lbs']} lbs")
        print(f"Cancer type: {user_data['cancer_type']}")

        # Weight history
        weight_history = db.get_weight_history(user_data['id'], limit=4)
        if weight_history:
            print(f"\nRecent weights:")
            for record in weight_history:
                print(f"  {record['date']}: {record['weight_lbs']} lbs")

        # Recent compliance
        compliance = db.get_compliance_history(user_data['id'], days=7)
        if compliance:
            avg_adherence = sum(r['adherence_percentage'] for r in compliance) / len(compliance)
            print(f"\n7-day adherence: {avg_adherence:.1f}%")

        # Research stats
        cursor = db.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM research_studies")
        study_count = cursor.fetchone()[0]
        print(f"\nResearch database: {study_count} studies")

        cursor.execute("SELECT COUNT(*) FROM foods")
        food_count = cursor.fetchone()[0]
        print(f"Foods in database: {food_count}")

        db.close()

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main CLI"""
    parser = argparse.ArgumentParser(
        description="No Colon, Still Rollin' - Anti-Cancer Food Protocol System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First time setup
  python src/main.py setup

  # Update research database
  python src/main.py update-research

  # Generate today's protocol
  python src/main.py protocol

  # Record weekly weight (Monday morning)
  python src/main.py weight 177

  # Track daily compliance
  python src/main.py track

  # Show compliance history
  python src/main.py history

  # Show current status
  python src/main.py status
        """
    )

    parser.add_argument(
        "--user",
        default="Jesse Mills",
        help="User name (default: Jesse Mills)"
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Setup
    subparsers.add_parser('setup', help='Initial setup')

    # Update research
    research_parser = subparsers.add_parser('update-research', help='Update research from PubMed')
    research_parser.add_argument('--max', type=int, default=20,
                                help='Max results per search (default: 20)')

    # Protocol
    protocol_parser = subparsers.add_parser('protocol', help='Generate daily protocol')
    protocol_parser.add_argument('--weight', type=float, help='Current weight in lbs')

    # Weight
    weight_parser = subparsers.add_parser('weight', help='Record weekly weight')
    weight_parser.add_argument('weight', type=float, help='Weight in pounds')

    # Track
    subparsers.add_parser('track', help='Track daily compliance')

    # History
    history_parser = subparsers.add_parser('history', help='Show compliance history')
    history_parser.add_argument('--days', type=int, default=7, help='Days to show (default: 7)')

    # Status
    subparsers.add_parser('status', help='Show current status')

    args = parser.parse_args()

    # Execute command
    if args.command == 'setup':
        setup()

    elif args.command == 'update-research':
        update_research(max_per_search=args.max)

    elif args.command == 'protocol':
        generate_protocol(user=args.user, weight=args.weight)

    elif args.command == 'weight':
        record_weight(user=args.user, weight=args.weight)

    elif args.command == 'track':
        track_compliance(user=args.user)

    elif args.command == 'history':
        show_history(user=args.user, days=args.days)

    elif args.command == 'status':
        show_status(user=args.user)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
