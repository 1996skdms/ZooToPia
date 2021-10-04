from datetime import datetime

import pandas as pd
pd.set_option('display.max_columns', 1000)


class Dart:
    def __init__(self):
        pass

    def financial_info(self, dart, symbol):

        df_index = pd.DataFrame()
        for i in range(1, 5):
            last_year = datetime.today().date().year - i
            df = dart.finstate(corp=symbol, bsns_year=last_year)
            if i == 1:
                df_index = pd.concat([df_index, df['account_nm']], axis=1)
            index = ['thstrm_dt', 'thstrm_amount']
            if 'thstrm_dt' not in df.columns:
                continue

            df = df[index].rename(columns={'thstrm_dt': 'thstrm_dt_' + str(last_year)
                , 'thstrm_amount': 'thstrm_amount_' + str(last_year)})
            df_index = pd.concat([df_index, df], axis=1)

        linked_sales, separate_sales, revenue, asset, net_income, liability = {}, {}, {}, {}, {}, {}
        now_year = datetime.today().date().year

        for i, col in enumerate(df_index['account_nm']):
            if i > 12:
                break
            if col == '매출액':
                for k in range(1, 5):
                    last_year = now_year - k
                    if 'thstrm_amount_' + str(last_year) in df_index.columns:
                        linked_sales[str(last_year)] = df_index['thstrm_amount_' + str(last_year)][i].replace(',', '')
                    else:
                        linked_sales[str(last_year)] = 0

            if col == '영업이익':
                for k in range(1, 5):
                    last_year = now_year - k
                    if 'thstrm_amount_' + str(last_year) in df_index.columns:
                        revenue[str(last_year)] = df_index['thstrm_amount_' + str(last_year)][i].replace(',', '')
                    else:
                        revenue[str(last_year)] = 0

            if col == '자본총계':
                for k in range(1, 5):
                    last_year = now_year - k
                    if 'thstrm_amount_' + str(last_year) in df_index.columns:
                        asset[str(last_year)] = df_index['thstrm_amount_' + str(last_year)][i].replace(',', '')
                    else:
                        asset[str(last_year)] = 0

            if col == '당기순이익':
                for k in range(1, 2):
                    last_year = now_year - k
                    if 'thstrm_amount_' + str(last_year) in df_index.columns:
                        net_income[str(last_year)] = df_index['thstrm_amount_' + str(last_year)][i].replace(',', '')
                    else:
                        net_income[str(last_year)] = 0

            if col == '부채총계':
                for k in range(1, 2):
                    last_year = now_year - k
                    if 'thstrm_amount_' + str(last_year) in df_index.columns:
                        liability[str(last_year)] = df_index['thstrm_amount_' + str(last_year)][i].replace(',', '')
                    else:
                        liability[str(last_year)] = 0

        for i in range(21, 25):
            if df_index['account_nm'][i] == '매출액':
                for k in range(1, 5):
                    last_year = now_year - k
                    if 'thstrm_amount_' + str(last_year) in df_index.columns:
                        separate_sales[str(last_year)] = df_index['thstrm_amount_' + str(last_year)][i].replace(',', '')
                    else:
                        separate_sales[str(last_year)] = 0
                break

        ret = {'linked_sales': linked_sales, 'separate_sales': separate_sales, 'revenue': revenue, 'asset': asset, 'net_income': net_income, 'liability': liability}

        df_rep = dart.report(symbol, '배당', now_year - 1)

        if 'thstrm' in df_rep.columns:
            ret['odds'] = df_rep['thstrm'][7]
            ret['odds_cash'] = df_rep['thstrm'][11]
        else:
            ret['odds'] = 0
            ret['odds_cash'] = 0

        print(ret)
        return ret


dart_service = Dart()