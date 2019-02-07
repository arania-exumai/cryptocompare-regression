import certifi, hashlib, json, lxml.html, math, pdftotext, requests
import requests

from datetime import *
from etherscan.contracts import Contract

#terminal cosmetics
bolden = '\033[1m'
end_formatting = '\033[0m'
maybe_blue = '\033[94m'
okay_green = '\033[92m'
certain_cyan = '\u001b[36m'
dirty_yellow = '\u001b[33m'
danger_red = '\u001b[31m'


def gather_statements(statements_url, timeframe='daily'):
    statements_url = 'https://stasis.net/daily-statements/'

    res = requests.get(daily_statements_url)
    doc = lxml.html.fromstring(res.content)
    table_rows = doc.xpath('//table[@class="daily-statement__table"]/tr')
    len_rows = len(table_rows)
    print(len_rows)

    pdf_urls = doc.xpath('//table[@class="daily-statement__table"]/tr//td[@class="daily-statement__table-cell daily-statement__table-cell_download"]/a/@href')
    pdf_count = len(pdf_urls)
    print(f'Number of PDF Statements: {certain_cyan + str(pdf_count) + end_formatting}\n')

    filenames_downloaded = []
    for ind, statement_url in enumerate(pdf_urls):
        res = requests.get(statement_url)
        filename = "statements/%s_%s.pdf" % (timeframe, str(ind))
        print("Saving %s" % filename)
        with open(filename, 'wb') as f:
            f.write(res.content)
        filenames_downloaded.append(filename)
        break

    return filenames_downloaded

daily_statements_url = 'https://stasis.net/daily-statements/'
daily_filenames = gather_statements(daily_statements_url)
print(daily_filenames)
weekly_statements_url = 'https://stasis.net/weekly-statements/'
weekly_filenames = gather_statements(weekly_statements_url, timeframe='weekly')
print(weekly_filenames)

raise



# Loads daily PDF statement
with open("daily_statement.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)
    pdf_length = (len(pdf))

bank1 = "Electronic Payments Association Ltd, England"
bank2 = "EXT Limited, Cyprus"
bank3 = "XNT Limited, Malta"

bank1_page = (pdf[0])
ending_balance_line = bank1_page.splitlines()[12]
epayment_ending_bal = float(ending_balance_line.split()[3])
dategen_epayment = bank1_page.splitlines()[11]
dategen_redacted = dategen_epayment.split()[-3:]
bank1_date = dategen_redacted[0]
bank1_time = dategen_redacted[1]
bank1_format = dategen_redacted[2]
bank1_datetime_input = bank1_date + ' ' + bank1_time + ' ' + bank1_format
bank1_object_timestamp = datetime.strptime(bank1_datetime_input, '%m/%d/%Y %I:%M:%S %p')
print(f'The bank balance at {bank1} is {bolden + "€ " + str(epayment_ending_bal) + end_formatting}, generated as of {maybe_blue + str(bank1_object_timestamp) + end_formatting}')

bank2_page = (pdf[1])
ending_balance_line2 = bank2_page.splitlines()[21]
ext_balance_string = ending_balance_line2.split()[2]
ext_commaless_bal = float(ext_balance_string.replace(',', ''))
dategen2_ext = bank2_page.splitlines()[10]
dategen2_redacted = dategen2_ext.split()[2]
bank2_datetime = datetime.strptime(dategen2_redacted, '%d.%m.%Y').date()
print(f'The bank balance at {bank2} is {bolden + "€ " + str(ext_commaless_bal) + end_formatting}, generated as of {bolden + str(bank2_datetime) + end_formatting}')

if (pdf_length == 6):
    bank3_page = (pdf[4])
else:
    bank3_page = (pdf[5])
ending_balance_line3 = bank3_page.splitlines()[16]
xnt_balance_string = ending_balance_line3.split()[2]
xnt_commaless_bal = float(xnt_balance_string.replace(',', ''))
dategen3_xnt = bank3_page.splitlines()[9]
dategen3_redacted = dategen3_xnt.split()[2]
bank3_datetime = datetime.strptime(dategen3_redacted, '%d.%m.%Y').date()
print(f'The bank balance at {bank3} is {bolden + "€ " + str(xnt_commaless_bal) + end_formatting}, generated as of {bolden + str(bank3_datetime) + end_formatting}\n')

total_bankstatement_balance = epayment_ending_bal + ext_commaless_bal + xnt_commaless_bal
print(f'The daily bank statement balance of Stasis totals to {maybe_blue + "€ " + str(total_bankstatement_balance) + end_formatting}\n')
    
# Loops through and loads weekly BDO verification files
for k in range(len(weekly_files_downloaded)):    
    with open(weekly_files_downloaded[k], "rb") as f:
        bdo_pdf = pdftotext.PDF(f)
    
    #extracts date of weekly report
    bdo_pg = (bdo_pdf[0])
    company_name = bdo_pg.splitlines()[0]
    company_substring = company_name.split()
    company_fullname = company_substring[-2] + " " + company_substring[-1]
    bdo_date = bdo_pg.splitlines()[23]
    bdo_split_date = bdo_date.split()[-3:]
    bdo_date_joined = bdo_split_date[0] + " " + bdo_split_date[1][:3] + " " + (bdo_split_date[2])[:-1]
    bdo_date_verification = datetime.strptime(bdo_date_joined, '%d %b %Y').date()
    print(f'For the week leading up to {bolden + str(bdo_date_verification) + end_formatting}, {danger_red} {company_fullname} {end_formatting} {bolden}verifies{end_formatting} the Stasis\' Account\n')

    #extracts first bank balance from weekly report
    epay_line = bdo_pg.splitlines()[26]
    epay_amt = float(epay_line.split()[10].replace(',', '')) 
    epay_eta = datetime.strptime((epay_line.split()[11]), '%H:%M').time()
    print(f'Balance at {bank1} to be {bolden + "€ " + str(epay_amt) + end_formatting} as of {maybe_blue + str(epay_eta)[:-3] + end_formatting}')

    #extracts second bank balance from weekly report
    ext_line = bdo_pg.splitlines()[28]
    ext_amt = float(ext_line.split()[9].replace(',', '')) 
    ext_eta = datetime.strptime((ext_line.split()[10]), '%H:%M').time()
    print(f'Balance at {bank2} to be {bolden + "€ " + str(ext_amt) + end_formatting} as of {maybe_blue + str(ext_eta)[:-3] + end_formatting}')

    #extracts third bank balance from weekly report
    xnt_line = bdo_pg.splitlines()[30]
    xnt_amt = float(xnt_line.split()[9].replace(',', '')) 
    xnt_eta = datetime.strptime((xnt_line.split()[10]), '%H:%M').time()
    print(f'Balance at {bank3} to be {bolden + "€ " + str(xnt_amt) + end_formatting} as of {maybe_blue + str(xnt_eta)[:-3] + end_formatting}\n')

    total_bdo_balance = epay_amt + ext_amt + xnt_amt
    print(f'Summing to a total FIAT Deposit of {maybe_blue + "€ " + str(total_bdo_balance) + end_formatting}\n')

    print(f'The discrepancy between the latest daily statement (Banks) and the weekly verification (Binder Dijker Otte) is {okay_green + "€ " + str(abs(total_bankstatement_balance - total_bdo_balance)) + end_formatting}\n')

    signatory = bdo_pg.splitlines()[41]
    position = bdo_pg.splitlines()[42]
    print(f'As Signed By {bolden + signatory + end_formatting}, {position}\n')

#checks current time
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
current_timestamp = (datetime.strptime(current_time,'%Y-%m-%d %H:%M:%S')) + timedelta(hours=5)

#calculates time since last daily statement produced
daily_tdelta = current_timestamp - bank1_object_timestamp
print (f'Current Timestamp is: {str(current_timestamp)}')
print (f'Latest Daily Statement Published at: {str(bank1_object_timestamp)}')
string_daily_time_delta = str(daily_tdelta)

#includes logic to handle timestamps where day is < 1
if "days" in string_daily_time_delta: 
    statement_d_delta = int((string_daily_time_delta)[0])
    statement_h_delta = int((string_daily_time_delta)[8:10])
else:
    statement_d_delta = 0
    statement_h_delta = int((string_daily_time_delta)[0:1])

statement_total_delta = (statement_d_delta*24) + statement_h_delta

if (statement_total_delta > 24):
    print(f'Total Hours Elapsed since latest bank statement {danger_red + str(statement_total_delta ) + end_formatting}')    
else:
    print(f'Total Hours Elapsed since latest bank statement {okay_green + str(statement_total_delta ) + end_formatting}')

#calculates time since last weekly verification conducted
weekly_timestamp = datetime.combine(bdo_date_verification, (max(*[ epay_eta, ext_eta, xnt_eta])))
wk_tdelta = current_timestamp - weekly_timestamp

verification_d_delta = int((str(wk_tdelta))[0])
verification_h_delta = int((str(wk_tdelta))[8:10])
verification_total_delta = (verification_d_delta*24) + verification_h_delta
if (verification_total_delta > 168):
    print(f'Total Hours Elapsed since latest BDO verification {danger_red + str(verification_total_delta) + end_formatting}\n')
else:
    print(f'Total Hours Elapsed since latest BDO verification {okay_green + str(verification_total_delta) + end_formatting}\n')

'''
#extracts embedded images from pdf
for x in range(len(weekly_files_downloaded)):
    doc = fitz.open(weekly_files_downloaded[x])
    print ("Extracting embedded PNGs including Signatures...13%..37%.......84%...100%..completed.\n")
    for i in range(len(doc)):    
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n < 5:       # this is GRAY or RGB
                pix.writePNG("p%s-%s.png" % (i, xref))
            else:               # CMYK: convert to RGB first
                pix1 = fitz.Pixmap(fitz.csRGB, pix)
                pix1.writePNG("p%s-%s.png" % (i, xref))
                pix1 = None
            pix = None
'''

#extracts total supply of stablecoin
etherscan_api_key = 'VMQHQB1R4TSJ6E9CVP55ECHMAWXV5VXCPX'
token_contract_address = '0xdb25f211ab05b1c97d595516f45794528a807ad8'
stasis_etherscan = "https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress="+token_contract_address+"&apikey="+etherscan_api_key
etherscan_response = requests.get(stasis_etherscan, verify=certifi.where())
response_jsonify = etherscan_response.json()

total_supply_stasis = (int(response_jsonify.get("result")))/100
print(f'As per Etherscan, Stasis EURS Token Total Supply: {maybe_blue + str({str(total_supply_stasis)[:-2]}) + end_formatting} \n')

print(f'The discrepancy between the latest daily statement (Banks) and the total coin supply on the blockchain (Ethereum) is {okay_green + "€ " + str(abs(total_supply_stasis - total_bankstatement_balance)) + end_formatting}\n')
print(f'The discrepancy between the latest weekky verification (BDO) and the total coin supply on the blockchain (Ethereum) is {okay_green + "€ " + str(abs(total_supply_stasis - total_bdo_balance)) + end_formatting}\n')

#get solidity source code for Stasis' token contract and checks sha-256 hash
api = Contract(address=token_contract_address, api_key=etherscan_api_key)
sourcecode = api.get_sourcecode()
solidity_state = sourcecode[0]['SourceCode']
sol_hash = hashlib.sha256(solidity_state.encode('utf-8')).hexdigest()
print (f'Sha-256 Hash of Stasis Solidity Contract is: {dirty_yellow + sol_hash + end_formatting}\n')
#print (solidity_state)


#uses coincmarketcap's free keys to retrive information about stasis from all new pro api
stasis_cmc_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=2989"
headers = {'X-CMC_PRO_API_KEY': '6ab59890-e6c8-4f77-830a-ae6142e34a7c'}

r = requests.get(stasis_cmc_url,headers=headers)
cmc_jsonified = r.json()
pretty_print_cmc = json.dumps(cmc_jsonified, indent=2)

stasis_cmc_id = cmc_jsonified['data']['2989']['id']
stasis_cmc_name = cmc_jsonified['data']['2989']['name']
stasis_cmc_rank = cmc_jsonified['data']['2989']['cmc_rank']
stasis_cmc_symbol = cmc_jsonified['data']['2989']['symbol']
stasis_cmc_query_timestamp = cmc_jsonified['status']['timestamp']
stasis_cmc_date_added = cmc_jsonified['data']['2989']['date_added']
stasis_cmc_total_supply = cmc_jsonified['data']['2989']['total_supply']
stasis_cmc_last_updated = cmc_jsonified['data']['2989']['last_updated']
stasis_cmc_market_pairs = cmc_jsonified['data']['2989']['num_market_pairs']
stasis_cmc_usd_price = cmc_jsonified['data']['2989']['quote']['USD']['price']
stasis_cmc_market_cap = cmc_jsonified['data']['2989']['quote']['USD']['market_cap']
stasis_cmc_24h_volume = cmc_jsonified['data']['2989']['quote']['USD']['volume_24h']
stasis_cmc_circulating_supply = cmc_jsonified['data']['2989']['circulating_supply']
stasis_cmc_underlying_blockchain = cmc_jsonified['data']['2989']['platform']['name']
stasis_cmc_1h_percent_change = cmc_jsonified['data']['2989']['quote']['USD']['percent_change_1h']
stasis_cmc_7d_percent_change = cmc_jsonified['data']['2989']['quote']['USD']['percent_change_7d']
stasis_cmc_24h_percent_change = cmc_jsonified['data']['2989']['quote']['USD']['percent_change_24h']

print (f'Total Supply of {maybe_blue + str(stasis_cmc_name) + end_formatting} from {dirty_yellow} + (Coinmarketcap): + {end_formatting } {maybe_blue + str(stasis_cmc_total_supply) + end_formatting} last updated {maybe_blue + str(stasis_cmc_last_updated) + end_formatting}')

#uses cryptocompares's free keys to retrive information about stasis as a second market aggregator source
stasis_cryptocompare_ohlcv = "https://min-api.cryptocompare.com/data/histoday?fsym=EURS&tsym=EUR&limit=146"
'''
cryptocompare_stasis = "https://min-api.cryptocompare.com/data/coin/generalinfo?fsyms=EURS&tsym=USD"
cryptocompare_req = requests.get(cryptocompare_stasis)
cryptocompare_jsonified = cryptocompare_req.json()
pretty_print_cryptocompare = json.dumps(cryptocompare_jsonified, indent=2)
print (pretty_print_cryptocompare)
'''
