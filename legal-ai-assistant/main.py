import os
from summarizer.planner import Planner          # changed from agents
from summarizer.preprocessor import Preprocessor
from summarizer.summarizer import Summarizer
from dotenv import load_dotenv

class LegalAIAssistant:
    """
    Main orchestrator for the Legal AI Assistant
    Now includes Summarizer Agent
    """
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize agents
        self.planner = Planner()
        self.preprocessor = Preprocessor()
        self.summarizer = Summarizer()
        
        print("=" * 60)
        print("LEGAL AI ASSISTANT - WITH SUMMARIZER")
        print("=" * 60)
        print("Fine-Tuned Llama-3 (10k+ Data) via Colab API")
        print("=" * 60)
    
    def process_document(self, file_path: str):
        """
        Main pipeline to process a legal document
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return
        
        print(f"\nProcessing document: {os.path.basename(file_path)}")
        print("-" * 40)
        
        # Step 1: Planning
        print("\n[STEP 1] PLANNING")
        print("-" * 20)
        plan = self.planner.plan(file_path)
        
        if not plan.get("success"):
            print(f"Planning failed: {plan.get('error')}")
            return plan
        
        print(f"✓ Document type: {plan['document_type']}")
        print(f"✓ Agent sequence: {' → '.join(plan['agent_sequence'])}")
        print(f"✓ Next agent: {plan['next_agent']}")
        
        # Initialize results dictionary
        results = {
            "plan": plan,
            "preprocessing": None,
            "summarization": None
        }
        
        # Step 2: Execute based on plan
        print(f"\n[STEP 2] EXECUTION")
        print("-" * 20)
        
        # Track what document text we have for summarization
        document_text_for_summary = ""
        extracted_info_for_summary = {}
        
        # Check if we need preprocessor
        if plan['next_agent'] == 'preprocessor':
            print("Running Preprocessor...")
            preprocess_result = self.preprocessor.process(file_path)
            results["preprocessing"] = preprocess_result
            
            if preprocess_result.get("success"):
                print("✓ Preprocessing completed successfully!")
                
                # Extract text for summarization
                document_text_for_summary = preprocess_result.get("original_text", "")
                extracted_info_for_summary = preprocess_result.get("extracted_info", {})
                
                print(f"\nExtracted Information:")
                print("-" * 30)
                info = extracted_info_for_summary
                print(f"Case Number: {info.get('case_number', 'N/A')}")
                print(f"Court: {info.get('court_name', 'N/A')}")
                print(f"Judge: {info.get('judge_name', 'N/A')}")
                print(f"Date: {info.get('date', 'N/A')}")
                print(f"Legal Sections: {', '.join(info.get('sections_mentioned', [])[:3])}")
                
                print(f"\nDocument Statistics:")
                print(f"Word Count: {preprocess_result.get('word_count', 0)}")
                
                print(f"\nReady for next agent: SUMMARIZER")
            else:
                print(f"✗ Preprocessing failed: {preprocess_result.get('error')}")
                return results
        
        elif plan['next_agent'] == 'summarizer':
            print(f"Document type '{plan['document_type']}' detected.")
            print("Skipping preprocessor, reading document directly...")
            
            # Read document directly for summarization
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    document_text_for_summary = f.read()
                print(f"✓ Read document directly ({len(document_text_for_summary)} chars)")
            except Exception as e:
                print(f"✗ Error reading document: {e}")
                return results
        
        # Step 3: Summarization (if we have text)
        if document_text_for_summary:
            print(f"\n[STEP 3] SUMMARIZATION")
            print("-" * 20)
            print("Generating summary using Fine-Tuned Llama-3 (Colab)...")
            
            # Prepare data for summarizer
            summarizer_data = {
                "document_type": plan['document_type'],
                "text": document_text_for_summary,
                "extracted_info": extracted_info_for_summary
            }
            
            # Call summarizer
            summary_result = self.summarizer.summarize(summarizer_data)
            results["summarization"] = summary_result
            
            if summary_result.get("success"):
                print("✓ Summarization completed successfully!")
                summary_text = summary_result.get("summary", "")
                
                print(f"\nSUMMARY:")
                print("=" * 60)
                print(summary_text)
                print("=" * 60)
                
                # Compute statistics locally
                original_len = len(document_text_for_summary)
                summary_len = len(summary_text)
                compression = (1 - summary_len / original_len) * 100 if original_len > 0 else 0
                
                print(f"\nSummary Statistics:")
                print(f"Original length: {original_len} chars")
                print(f"Summary length: {summary_len} chars")
                print(f"Compression: {compression:.1f}% reduction")
                print(f"Model used: {summary_result.get('model_used', 'N/A')}")
                
                print(f"\nReady for next agent: FORMATTER")
            else:
                print(f"✗ Summarization failed: {summary_result.get('error')}")
        
        return results


def create_sample_files():
    """Create sample legal documents for testing"""
    samples_dir = "sample_docs"
    os.makedirs(samples_dir, exist_ok=True)
    
    # Sample judgement document (more detailed)
    judgement_text = """Appeal No. LXVI of 1949.
Appeal from the High Court of judicature, Bombay, in a reference under section 66 of the Indian Income tax Act, 1022.
K.M. Munshi (N. P. Nathvani, with him), for the appel lant. ' M.C. Setalvad, Attorney General for India (H. J. Umrigar, with him), for the respondent. 1950.
May 26.
The judgment of the Court was delivered by MEHR CHAND MAHAJAN J.
This is an appeal against a judgment of the High Court of Judicature at Bombay in an income tax matter and it raises the question whether munici pal property tax and urban immoveable property tax payable under the relevant Bombay Acts are allowable deductions under section 9 (1) (iv) of the Indian Income tax Act.
The assessee company is an investment company deriving its income from properties in the city of Bombay.
For the assessment year 1940 41 the net income of the assessee under the head "property" was computed by the Income tax Officer in the sum of Rs. 6,21,764 after deducting from gross rents certain payments.
The company had paid during the relevant year Rs. 1,22,675 as municipal property tax and Rs. 32,760 as urban property tax.
Deduction of these two sums was claimed under the provisions of section 9 the Act.
Out of the first item a deduction in the sum of Rs. 48,572 was allowed on the ground that this item represented tenants ' burdens paid by the assessee, otherwise the claim was disal lowed.
The, appeals of the assessee to the Appellate As sistant Commissioner and to the Income tax Appellate Tribu nal were unsuccessful.
The Tribunal, however, agreed to refer two questions of law to the High Court of Judicature at Bombay, namely, (1) Whether the municipal taxes paid by the applicant company are an allowable deduction under 555 the provisions of section 9 (1) (iv) of the Indian Income tax Act; (2) Whether the urban immoveable property taxes paid by the applicant company are an allowable deduction under section 9 (1) (iv) or under section 9 (1) (v) of the Indian Income tax Act.
A supplementary reference was made covering a third question which was not raised before us and it is not there fore necessary to refer to it.
The High Court answered all the three questions in the negative and hence this appeal.
The question for our determination is whether the munic ipal property tax and urban immoveable property tax can be deducted as an allowance under clause (iv) of sub section (1) of section 9 of the Act.
The decision of the point depends firstly on the construction of the language employed in sub clause (iv) of sub section (1) of section 9 of the Act, and secondly, on a finding as to the true nature and character of the liability of the owner under the relevant Bombay Acts for the payment of these taxes.
Section 9 along with the relevant clause runs thus: (1) The tax shall be payable by an assessee under the head ' income from property ' in respect of the bona fide annual value of property consisting of any buildings or lands appurtenant thereto of Which he is the owner, . . subject to the following allowances, namely : (iv) where the property is subject to a mortgage or other capital charge, the amount of any interest on such mortgage or charge; where the property is subject to an annual charge not being a capital charge, the. amount of such charge; where the property is subject to a ground rent, the amount of such ground rent; and, where the property has been acquired, constructed, repaired, renewed or recon structed with borrowed capital, the amount of any interest payable on such capital; . . . " It will be seen that clause (iv) consists of four sub clauses corresponding to the four deductions allowed 556 under the clause.
Before the amending Act of 1939, clause (iv) contained only the first, third and fourth sub clauses.
Under the first sub clause interest is deductible whether the amount borrowed on the security of the property was spent on the property or not.
There is no question of any capital or other expenditure on the property.
The expression "capital charge" in the sub clause cannot connote a charge on the capital, that is, the property assessed.
That would be a redundancy as the opening words themselves clearly indicate that the charge is on the property.
We are therefore of opinion that capital charge here could only mean a charge created for a capital sum, i.e., a charge to secure the discharge of a liability of a capital nature.
In 1933 the Privy Council decided the case of Bijoy Singh.
Dudhuria vs Commissioner of Income tax, Calcutta (1 ).
It was not an assessment under section 9 but an assess ment on the general income of an assessee who was liable to pay maintenance for his step mother which had been charged on all his assets by a decree of Court.
It was not a li ability voluntarily incurred by him but one cast on him by law.
The Privy Council held that the amount paid by him in discharge of that liability formed no part of his real income and so should not be included in his assessment.
Though the decision proceeded on the principle that the outgoings were not part of the assessee 's income at all, the framers of the amending Act of 1939 wanted, apparently, to extend the principle, so far as the assessment of property was concerned, even to cases where obligatory payments had to be made out of the assessee 's income from the property charged with such payments, and the second sub clause, namely, "where the property is subject to an annual charge not being a capital charge, the amount of such charge" was added.
It is this sub clause which the appellant invokes in support of its claim to deduction of the municipal and urban, property taxes in the present case.
In view of the opening words of the newly added sub clause, the expression "capital charge" also used therein cannot have reference to a charge on the property, and we think it must (1) I.L.R. 60 cal.
557 be understood in the same sense as in sub clause (1); that is to say, the first sub clause having provided for deduc tion of interest where a capital sum is charged on the property, this sub clause provides for a deduction of annual sums so charged, such sums not being capital sums, the limiting words being intended to exclude cases where capital raised on the security of the property is made repayable in instalments.
In Commissioner of Income tax, Bombay vs Mahomedbhoy Rowji (1), a Bench of the Bombay High Court considered the meaning of these words.
As regards "annual charge," Beau mont C.J. observed as follows : "The words, I think, would cover a charge to secure an annual liability." Kania J., as he then was, said as follows : "I do not see how a charge can be annual unless it means a charge in respect of a payment to be made annually." This construction of the words has been followed in the judgment under appeal.
In Gappumal Kanhaiya Lal vs Commissioner of Income tax (2) (the connected appeal before us), the Bench of the Allahabad High Court agreed with the construction placed on these words in the Bombay case, i.e., the words "annual charge" mean a charge to secure an annual liability.
It is therefore clear that there is no conflict of judicial deci sions as to the meaning of the phrase "annual charge" occur ring in section 3 (1) (iv) and the meaning given is the natural meaning of these words.
As to the phrase "capital charge", Beaumont C.J. in the case above referred to took the view that the words mean a charge on capital.
Kania J., however, took a different view and observed that he was not prepared to accept the sugges tion that a document which provides for a certain payment to be made monthly or annually and charged on immoveable property or the estate of an individual becomes a capital charge.
In the Allahabad judgment under appeal these (1) I.L.R. (2) I.L.R. 1944 All.
558 words were considered as not meaning a charge on capital.
It was said that if an annual charge means a charge to secure the discharge of an annual liability, then, capital charge means a charge to secure the discharge of a liability of a capital nature.
We think this construction is a natu ral construction of the section and is right.
The determination of the point whether the taxes in dispute fall within the ambit of the phrase "annual charge not being a capital charge" depends on the provisions of the statutes under which they are levied.
Section 143 of the City of Bombay Municipal Act, 1888, authorises the levy of a general tax on all buildings and lands in the city.
The primary responsibility to pay this property tax is on the lessor (vide section 146 of the Act).
In order to assess the tax provision has been made for the determination of the annual rateable value of the building in section 154.
Section 156 provides for the maintenance of an assessment book in which entries have to be made every official year of all buildings in the city, their rateable value, the names of persons primarily liable for payment of the property tax on such buildings and of the amount for which each building has been assessed.
Section 167 lays down that the assess ment book need not be prepared every official year but public notices shall be given in accordance with sections 160 to 162 every year and the provisions o+ the said sec tions and of sections 163 and 167 shall be applicable each year.
These sections lay down a procedure for hearing objections and complaints against entries in the assessment book.
From these provisions it is clear ' that the liabil ity for the tax is determined at the beginning of each official year and the tax is an annual one.
It recurs from year to year.
Sections 143to 168 concern themselves with the imposition, liability and assessment of the tax for the year.
The amount of the tax for the year and the liability for its payment having been determined, the Act then pre scribes for its collection in the chapter "The collection of taxes.
" Section 197 provides that each of the property taxes shall be payable in 559 advance in half yearly instalments on each first day of April and each first day of October.
The provision as to half yearly instalment necessarily connotes an annual li ability.
In other words, it means that the annual liability can be discharged by half yearly payments.
Procedure has also been prescribed for recovery of the instalments by presentment of a bill, a notice of demand and then distress, and sale.
Finally section 212 provides as follows : "Property taxes due under this Act in respect of any building or land shall, subject to the prior payment of the land revenue, if any, due to the provincial ,Government thereupon, be a first charge . . upon the said build ing or land . " It creates a statutory charge on the building.
Urban immove able property tax is leviable under section 22 of Part VI of the Bombay Finance Act, 1932,on the annual letting value of the property.
The duty to collect the tax is laid on the municipality and it does so in the same manner as in the case of the municipal property tax.
Section 24 (2) (b) is in terms similar to section 212 of the Bombay Municipal Act.
It makes the land or the building security for the payment of this tax also.
For the purposes of section 9 of the Indian Income tax Act both these taxes, namely, the munici pal property tax as well as the urban immoveable property tax are of the same character and stand on the same foot ing.
Mr. Munshi, the learned counsel for the appellant con tended that both the taxes are assessed on the annual value of the land or the building and are annual taxes, although it may be that they are collected at intervals of six months for the sake of convenience, that the income tax itself is assessed on an annual basis, that in allowing deductions all payments made or all liabilities incurred during the previ ous year of assessment should be allowed and that the taxes in question fell clearly within the language of section 9 (1) (iv).
The learned Attorney General, on the other hand, argued that although the taxes are assessed for the year the liability to pay them arises at the beginning 560 of each half year and unless a notice of demand is issued and a bill presented there is no liability to pay them and that till then no charge under section 212 of the Act could possibly arise and that the liability to pay being half yearly in advance, the charge is not an annual charge.
It was also suggested that the taxes were a capital charge in the sense of the property being security for the payment.
We are satisfied that the contentions raised by the learned Attorney General are not sound.
It is apparent from the whole tenor of the two Bombay Acts that the taxes are in the nature of an annual levy on the property ' and are assessed on the annual value of the property each year.
The annual liability can be discharged by half yearly instalments.
The liability being an annual one and the property having been subjected to it, the provisions of clause (iv) of sub sec tion (1) of section 9 are immediately attracted.
Great emphasis was laid on the word"due" used in section 212 of the Municipal Act and it was said that as the taxes do not become due under the Act unless the time for the payment arrives, no charge comes into existence till then and that the charge is not an annual charge.
We do not think that this is a correct construction of section 212.
The words "property taxes due under this Act" mean property taxes for which a person is liable under the Act.
Taxes payable during the year have been made a charge on the property.
The liability and the charge both co exist and are co exten sive.
The provisions of the Act affording facilities for the discharge of the liability do not in any way affect their true nature and character.
If the annual liability is not discharged in the manner laid down by section 197, can it be said that the property cannot be sold for recovery of the whole amount due for the year ? The answer to this query can only be in the affirmative, i.e., that the proper ty is liable to sale.
In Commissioner of Income tax, Bombay vs Mahomedbhoy Rowji(1) Beaumont C.J., while rejecting the claim for the deduction of the taxes, placed reliance on (1) I.L.R. 561 section 9 (1) (v) which allows a deduction in respect of any sums paid on account of land revenue.
It was observed that land revenue stands on the same footing as municipal taxes and that as the legislature made a special provision for deduction of sums payable in regard to land revenue but not in respect of sums paid on account of municipal taxes that circumstance indicated that the deduction was not allowable.
For the same purpose reference was also made to the provi sions of section 10 which deal with business allowances and wherein deduction of any sum paid on account of land reve nue, local rates or municipal taxes has been allowed.
In the concluding part of his judgment the learned Chief Jus tice said that it was not necessary for him to consider what the exact meaning of the words was and that it was suffi cient for him to say that it did not cover municipal taxes which are made a charge on the property under section 212 of the Bombay Municipal Act.
Without determining the exact meaning of the words used by the statute it seems to us it was not possible to arrive at the conclusion that the taxes were not within the ambit of the clause.
It is elementary that the primary duty of a Court is to give effect to the intention of the legislature as expressed in the words used by it and no outside consideration can be called in aid tO find that intention.
Again reference to clause (v) of the section is not very helpful because land revenue is a charge of a paramount nature on all buildings and lands and that being so, a deduction in respect of the amount was mentioned in express terms.
Municipal taxes, on the other hand, do not stand on the same footing as land revenue.
The law as to them varies from province to province and they may not be necessarily a charge on property in all cases.
The legis lature seems to have thought that so far as municipal taxes on property are concerned, if they fall within the ambit of clause (iv), deduction will be claimable in respect of them but not otherwise.
The deductions allowed in section 10 under the head "Income from business" proceed on a different footing and a construction of section 9 with the aid of section 10 is apt to mislead.
562 Kania J. in the above case in arriving at his conclusion was influenced by the consideration that these taxes were of a variable character, i.e., liable to be increased or re duced under the various provisions of the Municipal Act and that the charge was in the nature of a contingent charge.
With great respect, it may be pointed out that all charges in a way may be or are of a variable and contingent na ture.
If no default is made, no charge is ever enforceable and whenever there is a charge, it can be increased or reduced during the year either by payment or by additional borrowing.
In Moss Empires Ltd. vs Inland Revenue Commissioners (1) it was held by the House of Lords that the fact that certain payments were contingent and variable in amount did not affect their character of being annual payments and that the word, "annual" must be taken to have the quality of being recurrent or being capable of recurrence.
In Cunard 's Trustees vs Inland Revenue Commissioners (2) it was held that the payments were capable of being recur rent and were therefore annual payments within the meaning of schedule D, case III, rule 1 (1), even though they were not necessarily recurrent year by year and the fact that they varied in amount was immaterial.
The learned Attorney General in view of these decisions did not support the view expressed by Kania J. Reliance was placed on a decision of the High Court of Madras in Mamad Keyi vs Commissioner of Income tax, Madras(3), in which moneys paid as urban immoveable property tax under the Bombay Finance Act were disallowed as inadmis sible under section 9 (1) (iv) or 9 (1) (v) of the Indian Income tax Act. 'This decision merely followed the view expressed in Commissioner of income tax, Bombay vs Mahomedb hoy Rowji (4)and was not arrived at on any independent or fresh reasoning and is not of much assistance in the deci sion of the case.
The Allahabad High Court (1) (2) [1948] 1 A.E.R. 150. (3) I.L.R. (4) I.L.R. 563 in Gappumal Kanhaiya Lal vs Commissioner of Incometax (1) (the connected appeal) took a correct view of this matter and the reasoning given therein has our approval.
The result is that this appeal is allowed and the two questions which were referred to the High Court by the Income tax Tribunal and cited above are answered in the affirmative.
The appellants will have their costs in the appeal.
Appeal allowed.
"""
    # Sample bail document
    bail_text = """IN THE COURT OF THE ADDITIONAL SESSIONS JUDGE, DELHI

BAIL APPLICATION NO. 456/2023

APPLICANT: MR. AMIT SHARMA
VERSUS
STATE: NCT OF DELHI

APPLICATION FOR GRANT OF REGULAR BAIL

The applicant respectfully submits:

1. That the applicant has been falsely implicated in FIR No. 789/2023 registered at Police Station Dwarka, Delhi under Sections 406 and 420 IPC.

2. That the applicant is a law-abiding citizen with no criminal antecedents and has deep roots in society.

3. That the investigation is complete and chargesheet has been filed.

4. That the applicant is not a flight risk and will cooperate with the trial.

5. That the applicant is ready to abide by any conditions imposed by this Hon'ble Court.

GROUNDS FOR BAIL:
a) The offense alleged is triable by Magistrate and not punishable with death or life imprisonment.
b) The applicant has permanent residence and family in Delhi.
c) Custodial interrogation is not required as investigation is complete.
d) The applicant is willing to furnish surety.

LEGAL PROVISIONS:
The application is filed under Section 439 of the Code of Criminal Procedure, 1973.

PRAYER:
In view of the above, it is prayed that regular bail may be granted to the applicant on suitable terms and conditions.

VERIFICATION:
I, Amit Sharma, s/o Sh. Ramesh Sharma, do hereby verify that the contents of paragraphs 1 to 5 are true to my knowledge and I believe no part of it is false."""
    
    # Write sample files
    judgement_path = os.path.join(samples_dir, "sample_judgement.txt")
    bail_path = os.path.join(samples_dir, "sample_bail.txt")
    
    with open(judgement_path, 'w', encoding='utf-8') as f:
        f.write(judgement_text)
    
    with open(bail_path, 'w', encoding='utf-8') as f:
        f.write(bail_text)
    
    print(f"Sample files created in '{samples_dir}' folder:")
    print(f"  - {judgement_path}")
    print(f"  - {bail_path}")
    
    return [judgement_path, bail_path]


def main():
    """Main function to run the assistant"""
    assistant = LegalAIAssistant()
    
    # Create sample documents for testing
    sample_files = create_sample_files()
    
    # Test with sample documents
    for file_path in sample_files:
        print("\n" + "=" * 60)
        print(f"PROCESSING: {os.path.basename(file_path)}")
        print("=" * 60)
        
        result = assistant.process_document(file_path)
        
        # Wait for user to continue
        if file_path != sample_files[-1]:
            input("\nPress Enter to process next document...")


if __name__ == "__main__":
    main()