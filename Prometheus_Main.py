import  prometheus as prom
import Prometheus_Parameters as Parameters

def main():

    prom.create_csv_file(Parameters.CSV_File_PATH)
    NEXT_PAGE_EXISTS = True
    browser = prom.login()
    browser = prom.search_for_the_keyword(browser)
    page_number = 86

    while (NEXT_PAGE_EXISTS):

        prom.go_to_page_number(browser, page_number)
        flag = input("If ready for next page, enter any key except 'x'...")
        if (flag != 'x'):
            prom.append_metadata_to_CSV(prom.extract_items_metadata(browser))
            page_number += 1
            NEXT_PAGE_EXISTS = True

        else:
            NEXT_PAGE_EXISTS = False
    #prom.browser_quit(browser)

    
if __name__ == '__main__':
    main()