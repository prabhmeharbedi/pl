from pathlib import Path
import json
from typing import Dict, Any

from agents import TenancyFAQAgent
from agent_manager import AgentManager

def load_initial_knowledge():
    """Load initial knowledge for the tenancy FAQ agent."""
    try:
        # Get the knowledge directory
        knowledge_dir = Path(__file__).resolve().parent.parent / "knowledge"
        knowledge_dir.mkdir(exist_ok=True)
        
        # Create the tenancy FAQ knowledge directory
        tenancy_knowledge_dir = knowledge_dir / "tenancy"
        tenancy_knowledge_dir.mkdir(exist_ok=True)
        
        # Create or load initial knowledge
        sample_knowledge_file = tenancy_knowledge_dir / "sample_tenancy_knowledge.json"
        
        if not sample_knowledge_file.exists():
            # Create sample knowledge if it doesn't exist
            sample_knowledge = create_sample_knowledge()
            
            # Save the sample knowledge
            with open(sample_knowledge_file, "w") as f:
                json.dump(sample_knowledge, f, indent=2)
        else:
            # Load existing knowledge
            with open(sample_knowledge_file, "r") as f:
                sample_knowledge = json.load(f)
        
        # Get the tenancy agent from the manager
        agent_manager = AgentManager()
        tenancy_agent = agent_manager.tenancy_faq
        
        # Add the knowledge to the agent
        for doc_id, doc in sample_knowledge.items():
            tenancy_agent.add_knowledge_text(
                id=doc_id,
                title=doc["title"],
                content=doc["content"]
            )
        
        # Load the knowledge into the vector database
        tenancy_agent.load_knowledge()
        
        print(f"Successfully loaded {len(sample_knowledge)} knowledge documents for the tenancy FAQ agent")
        
    except Exception as e:
        print(f"Error loading initial knowledge: {str(e)}")
        raise

def create_sample_knowledge() -> Dict[str, Dict[str, str]]:
    """Create sample tenancy knowledge for the agent."""
    return {
        "notice_period": {
            "title": "Notice Periods for Tenancy Termination",
            "content": """
                # Notice Periods for Tenancy Termination
                
                ## General Rules
                
                Most residential tenancies require the tenant to provide notice before moving out. The standard notice periods are:
                
                - Month-to-month tenancies: 30 days notice (in most jurisdictions)
                - Fixed-term leases: Notice typically not required if ending on the lease end date
                - Early termination: Usually requires landlord agreement or special circumstances
                
                ## Special Circumstances
                
                Some situations may allow for shorter notice periods:
                
                1. Domestic violence situations
                2. Military deployment
                3. Uninhabitable living conditions
                4. Health and safety violations
                
                ## Location-Specific Information
                
                Notice periods vary by location. Always check local laws. Some examples:
                
                - California: 30 days for tenancies less than 1 year, 60 days for longer tenancies
                - New York: 30 days notice for tenancies under 1 year
                - UK: Usually 1 month for monthly tenancies
                - Australia: Typically 14-28 days depending on the state
                
                ## Best Practices
                
                1. Always provide written notice
                2. Deliver notice according to methods specified in your lease
                3. Keep a copy of the notice and proof of delivery
                4. Be specific about your move-out date
            """
        },
        "rent_increases": {
            "title": "Rent Increase Regulations",
            "content": """
                # Rent Increase Regulations
                
                ## During Fixed-Term Leases
                
                In most jurisdictions, landlords cannot increase rent during a fixed-term lease unless:
                
                1. The lease specifically allows for it
                2. The tenant agrees to the increase in writing
                3. There is a government-authorized increase
                
                ## For Month-to-Month Tenancies
                
                For month-to-month agreements, landlords typically must provide notice before increasing rent:
                
                - 30 days notice for increases under 10% (in many jurisdictions)
                - 60-90 days notice for larger increases (varies by location)
                
                ## Rent Control Areas
                
                Many cities have rent control or rent stabilization laws that limit:
                
                1. How much rent can be increased (often tied to inflation)
                2. How frequently increases can occur (typically once per year)
                3. What justifications are required for increases
                
                ## Best Practices for Tenants
                
                If you receive a rent increase notice:
                
                1. Check if it complies with local laws
                2. Verify proper notice was given
                3. Determine if your unit is subject to rent control
                4. Consider negotiating if the increase seems excessive
                5. Get any agreements in writing
            """
        },
        "security_deposits": {
            "title": "Security Deposit Return Process",
            "content": """
                # Security Deposit Return Process
                
                ## Timeframes for Return
                
                Most jurisdictions require landlords to return security deposits within:
                
                - 14-60 days after tenant moves out (varies by location)
                - California: 21 days
                - New York: 14 days
                - Florida: 15-60 days depending on whether tenant disputes deductions
                
                ## Allowable Deductions
                
                Landlords can typically deduct from security deposits for:
                
                1. Unpaid rent
                2. Damage beyond normal wear and tear
                3. Excessive cleaning costs
                4. Unpaid utilities
                5. Other lease violations with financial impact
                
                ## Tenant Rights
                
                Tenants generally have rights to:
                
                1. A detailed itemized statement of deductions
                2. Receipts for repairs or cleaning costs
                3. Interest on deposits (in some jurisdictions)
                4. Small claims court action if deposit is wrongfully withheld
                
                ## Best Practices
                
                To maximize return of a security deposit:
                
                1. Document condition at move-in and move-out with photos/video
                2. Request an initial inspection before moving out
                3. Clean thoroughly and repair minor damages
                4. Provide a forwarding address in writing
                5. Know local laws regarding what constitutes normal wear and tear
            """
        },
        "eviction_process": {
            "title": "Eviction Process and Tenant Rights",
            "content": """
                # Eviction Process and Tenant Rights
                
                ## Legal Grounds for Eviction
                
                Most jurisdictions require landlords to have legal cause for eviction, such as:
                
                1. Non-payment of rent
                2. Lease violations
                3. Property damage
                4. Illegal activities
                5. Expiration of lease (in some areas)
                6. Owner move-in (in some areas)
                
                ## Required Notice
                
                Landlords must provide written notice before beginning eviction proceedings:
                
                - Non-payment of rent: 3-10 days notice (varies by location)
                - Lease violations: 10-30 days notice to cure or vacate
                - No-fault evictions: 30-90 days notice (where permitted)
                
                ## The Legal Process
                
                Proper eviction requires:
                
                1. Written notice with specific reasons and timeframe
                2. Court filing if tenant doesn't comply with notice
                3. Court hearing where both parties can present their case
                4. Court judgment and order for eviction if landlord prevails
                5. Enforcement by sheriff/constable (not the landlord directly)
                
                ## Illegal Eviction Tactics
                
                Landlords CANNOT legally:
                
                1. Change locks without court order
                2. Remove tenant's belongings
                3. Shut off utilities
                4. Use threats or intimidation
                5. Remove doors or windows
                
                ## Tenant Defenses
                
                Possible defenses against eviction include:
                
                1. Improper notice or procedure
                2. Retaliation for reporting code violations
                3. Discrimination
                4. Acceptance of partial rent (in some cases)
                5. Failure to maintain habitable housing
            """
        }
    } 