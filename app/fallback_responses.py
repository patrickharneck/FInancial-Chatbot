# fallback_responses.py
"""
Smart fallback responses for when RAG retrieval confidence is low
Provides topic-specific templates in both English and Chichewa
"""


class FallbackResponses:
    """Generate smart fallback responses"""
    
    # Detailed Chichewa templates
    CHICHEWA_TEMPLATES = {
        'savings': """💰 **Kusunga Ndalama - Kufunika ndi Njira:**

Kusunga ndalama ndi njira yabwino kwambiri ya kupeza chitukuko cha ndalama. Anthu odziwika a ndalama amanena kuti "kulipira wekha ndi kofunika kwambiri".

**Chifukwa Chake Ndi Chofunika:**
- Chitetezo pa nthawi yovuta (matenda, mantha)
- Kugula zinthu zazikulu tsogolo lanu (nyumba, galimoto)
- Kukhala ndi mtendere wa maganizo
- Kukhala ndi ndalama za bizinesi

**Njira Zabwino za Kusunga:**
1. **Akaunti ya Banki** - NBS, Standard Bank, FDH - chiwongola dzanja 5-8% pa chaka
2. **Susu/Village Bank** - Kusunga limodzi ndi anzanu
3. **Mobile Money** - Mpamba/Airtel Money - zosavuta koma chiwongola dzanja pang'ono
4. **Treasury Bills** - Boma la Malawi - chiwongola dzanja 15-20% koma muyenera kukhala ndi K100,000 kapena zambiri

**Chitsanzo:** Musunga K5,000 sabata iliyonse (K20,000 pa mwezi). Pambuyo pa chaka chimodzi mudzakhala ndi K240,000!

📌 Chizindikiro: Yankho ili ndi lochokera ku chidziwitso cha ndalama.""",
        
        'budget': """📊 **Bajeti - Plan ya Ndalama:**

Bajeti ndi plan yomwe ikuthandizani kuona momwe ndalama zimayendere m'nyumba yanu. Pali njira yosavuta yotchedwa "50/30/20 rule":

**Gawo 1 - Zofunika (50%):**
Izi ndi zinthu zimene simungapeze nazo - chakudya, nyumba (rent), madzi, magetsi, transport. Ngati mumalandira K100,000 pa mwezi, K50,000 iyenera kupita ku zofunika izi.

**Gawo 2 - Zofuna (30%):**
Izi ndi zinthu zobwerera - entertainment, kudya kunja, zovala zatsopano. Izi zimatha kukhala K30,000.

**Gawo 3 - Kusunga (20%):**
Ndalama zoti musunga pa tsogolo - mwina K20,000 pa mwezi. Pambuyo pa chaka chimodzi mudzakhala ndi K240,000!

📌 Chizindikiro: Malangizo a ndalama.""",
        
        'loan': """🏦 **Ngongole (Loans) - Chidziwitso Chonse:**

Ngongole ndi ndalama zomwe mumabwereka ku banki kapena bungwe ndipo mumabweza ndi chiwongola dzanja (interest).

**Mitundu ya Ngongole:**
1. **Personal Loan** - Interest 25-35% pa chaka
2. **Salary Loan** - Interest 20-30%
3. **Business Loan** - Interest 18-28%
4. **Mortgage** - Interest 15-25%

**Zomwe Mumafuna:**
- ID (National ID kapena Passport)
- Mboni ya malipiro (payslip)
- Ndalama zoyambira (collateral)

📌 Chizindikiro: Yankho ili ndi lochokera ku chidziwitso cha ndalama.""",
        
        'fraud': """⚠️ **Chitetezo ku Chinyengo:**

Chinyengo cha ndalama ndi chovuta kwambiri ku Malawi tsopano.

**Njira za Kudziteteza:**
✅ **PIN Yanu = Ndalama Zanu** - Musapereke PIN kwa aliyense
✅ **Banki Sizimafunsa PIN pa Foni**
✅ **Onani Ma Links** - Musadindire links mu SMS
✅ **Fufuzani** - Funsani banki ngati mukukayikira

📌 Chizindikiro: Malangizo a chitetezo."""
    }
    
    # Detailed English templates
    ENGLISH_TEMPLATES = {
        'savings': """💰 **Complete Guide to Saving in Malawi:**

Saving money is the foundation of financial security and wealth building.

**Why Saving Matters:**
- Emergency Fund: Cover unexpected expenses without debt
- Financial Goals: Buy a house, start a business
- Peace of Mind: Reduce financial stress
- Wealth Building: Money saved can grow over time

**Best Savings Options:**
1. **Bank Savings Accounts** (NBS, Standard, FDH): 5-8% interest annually
2. **Fixed Deposits**: 10-15% interest, lock for 3-24 months
3. **Treasury Bills**: 15-20% interest, minimum MK100,000
4. **Village Banks (VSLA)**: Community-based, flexible

**Example:** Save MK10,000 weekly = MK520,000 after 1 year!

📌 Note: Based on general financial knowledge.""",
        
        'budget': """📊 **Creating a Budget:**

A budget helps you track income, control expenses, and achieve goals.

**The 50/30/20 Rule:**
- 50% for Needs: Rent, food, utilities, transport
- 30% for Wants: Entertainment, dining, shopping
- 20% for Savings: Emergency fund, investments

**Example:** Earn MK150,000 monthly:
- MK75,000 for needs
- MK45,000 for wants
- MK30,000 for savings

After 12 months: MK360,000 saved!

📌 Note: General budgeting guidance.""",
        
        'loan': """🏦 **Understanding Loans in Malawi:**

Loans are borrowed money that must be repaid with interest.

**Types of Loans:**
1. Personal Loan: 25-35% interest
2. Salary Loan: 20-30% interest
3. Business Loan: 18-28% interest
4. Mortgage: 15-25% interest

**Requirements:**
- National ID
- Proof of income (payslip)
- Collateral (for larger loans)

**Pro Tip:** Never borrow more than 30% of monthly income for repayments.

📌 Note: General loan information.""",
        
        'fraud': """⚠️ **Protection Against Fraud:**

Financial fraud is increasing in Malawi.

**How to Protect Yourself:**
✅ Never share PINs with anyone
✅ Banks never ask for PINs via phone
✅ Don't click suspicious links in SMS
✅ Verify unexpected calls claiming to be from banks
✅ Download official banking apps only from verified sources

**If Scammed:**
- Immediately freeze your account
- Report to police
- Warn others

📌 Note: Security best practices."""
    }
    
    @staticmethod
    def get_fallback(query: str, lang: str) -> str:
        """
        Get appropriate fallback response based on query topic
        
        Args:
            query: User query
            lang: Language code ('ny' or 'en')
            
        Returns:
            Fallback response string
        """
        query_lower = query.lower()
        
        # Select template dictionary based on language
        templates = (
            FallbackResponses.CHICHEWA_TEMPLATES if lang == 'ny' 
            else FallbackResponses.ENGLISH_TEMPLATES
        )
        
        # Match query to topic
        topic_keywords = {
            'savings': ['saving', 'save', 'kusunga', 'sunga', 'invest'],
            'budget': ['budget', 'plan', 'bajeti', 'kukonzekera'],
            'loan': ['loan', 'borrow', 'ngongole', 'kubwereka'],
            'fraud': ['fraud', 'scam', 'security', 'chinyengo', 'chitetezo']
        }
        
        # Find matching topic
        for topic, keywords in topic_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return templates.get(topic, FallbackResponses._get_generic(lang))
        
        # Return generic fallback
        return FallbackResponses._get_generic(lang)
    
    @staticmethod
    def _get_generic(lang: str) -> str:
        """Get generic fallback response"""
        if lang == 'ny':
            return """💡 **Malangizo a Ndalama:**

**1. Bajeti:** Lembani ndalama zomwe mumalandira ndi zomwe mumawononga. Gwiritsani ntchito "50/30/20 rule".

**2. Kusunga:** Sungani 10-20% ya ndalama zanu sabata iliyonse.

**3. Ngongole:** Musabwereke ndalama ngati situli kofunika kwambiri.

**4. Chitetezo:** Sungani PIN yanu bwino. Musadindire ma links osadziwika.

📌 Chizindikiro: Malangizo a ndalama."""
        
        else:
            return """💡 **Financial Guidance:**

**1. Budget:** Track income and expenses using the 50/30/20 rule.

**2. Save:** Aim for 10-20% of income weekly.

**3. Debt:** Avoid unnecessary borrowing.

**4. Security:** Never share PINs or click suspicious links.

📌 Note: General financial advice."""