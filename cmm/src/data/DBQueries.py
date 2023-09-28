
from cmm.models import Cmm_Warranty as Data2, Cmm_Warranty_New as Data3
from django.db.models import Q
from django.contrib import messages

from s2analytica.settings import START_TIME, END_TIME, IST
from datetime import datetime as dt
from cmm.models import Cmm_Sick as Data, Cmm_pro as Data1

class DBQuery:
    def sick_Head_graph_query(
        train_numbers,
        checked_coach_types,
        checked_coach_numbers,
        sick_heads,
        owning_rly,
        coach_status,
        department,
        vehicle_type,
        workshops,
        problem_start,
        problem_end,
        placement_start,
        placement_end,
        fit_start,
        fit_end,
        coach_count,
        sort_method,
    ):

        result_dict = {}
        result = list(
            Data.objects.filter(
                train_number__in=train_numbers,
                sick_head__in=sick_heads,
                owning_rly__in=owning_rly,
                coach_status__in=coach_status,
                department__in=department,
                vehicle_type__in=vehicle_type,
                coach_type__in=checked_coach_types,
                coach_number__in=checked_coach_numbers,
                workshop__in=workshops,
                problem_date__range=[
                    dt.strptime(f"{problem_start} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{problem_end} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],

                # already commented don't touch
                # placement_date__range=[
                #         f"{placement_start} 00:00:00+00:00",
                #         f"{placement_end} 23:59:00+00:00",
                # ],
                # fit_date__range=[
                #         f"{fit_start} 00:00:00+00:00",
                #         f"{fit_end} 23:59:00+00:00",
                # ],
            ).values_list("coach_number")
        )

        print(f"result: {result}")
        for r in result:
            if r[0] in result_dict:
                result_dict[r[0]] += 1
            else:
                result_dict[r[0]] = 1

        result = list(result_dict.items())
        result.sort(key=lambda x: x[1], reverse=True)
        table_res = result
        coach_number = []
        count = []
        for r in result:
            if r[0] != None:
                coach_number.append(int(r[0]))
                count.append(r[1])

        if coach_count != "":
            coach_number = coach_number[: int(coach_count)]
            count = count[: int(coach_count)]
            table_res = table_res[: int(coach_count)]

        if sort_method == "asc":
            coach_number.reverse()
            count.reverse()
            table_res.reverse()

        return [coach_number, count, table_res]

    def sick_Head_table_query(
        train_numbers,
        checked_coach_types,
        checked_coach_numbers,
        sick_heads,
        owning_rly,
        coach_status,
        department,
        vehicle_type,
        workshops,
        problem_start,
        problem_end,
        placement_start,
        placement_end,
        fit_start,
        fit_end,
        coach_count,
        sort_method,
    ):

        result_dict = {}
        result = list(
            Data.objects.filter(
                train_number__in=train_numbers,
                sick_head__in=sick_heads,
                owning_rly__in=owning_rly,
                coach_status__in=coach_status,
                department__in=department,
                vehicle_type__in=vehicle_type,
                coach_type__in=checked_coach_types,
                coach_number__in=checked_coach_numbers,
                workshop__in=workshops,
                problem_date__range=[
                    dt.strptime(f"{problem_start} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{problem_end} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
                # placement_date__range=[
                #         f"{placement_start} 00:00:00+00:00",
                #         f"{placement_end} 23:59:00+00:00",
                # ],
                # fit_date__range=[
                #         f"{fit_start} 00:00:00+00:00",
                #         f"{fit_end} 23:59:00+00:00",
                # ],
            ).values_list("coach_number")
        )

        for r in result:
            if r[0] in result_dict:
                result_dict[r[0]] += 1
            else:
                result_dict[r[0]] = 1

        result = list(result_dict.items())

        if sort_method == "asc":
            result.sort(key=lambda x: x[1], reverse=False)
        elif sort_method == "desc":
            result.sort(key=lambda x: x[1], reverse=True)

        if coach_count != "":
            return result[: int(coach_count)]
        return result

    def coach_pro_table_query(
         
        checked_coach_numbers,
         
        coach_number_box,
        sort_method,
    ):
         
        result_dict = {}
        result1 = list(
            Data1.objects.filter(    
                coach_number__in=checked_coach_numbers,
                
            ).values_list("coach_number")
        )
        result= result1

        if (coach_number_box!=""):
            result2 = list(
                Data1.objects.filter(  
                coach_number= coach_number_box,
                ).values_list("coach_number")
            )
            result+= result2

         

        for r in result:
            if r[0] in result_dict:
                result_dict[r[0]] += 0
            else:
                result_dict[r[0]] = 1

        result = list(result_dict.items())
        for i in range(len(result)):
            if str(result[i][0]) == "None":
                result.remove(result[i])
        if sort_method == "asc":
            result.sort(key=lambda x: x[0], reverse=False)
        elif sort_method == "desc":
            result.sort(key=lambda x: x[0], reverse=True)

        # if coach_count != "":
        #     return result[: int(coach_count)]
        # print(result)
        return result  

    def complain_type_query(
        request,
        problem_start,
        problem_end,
        complain,
        coach_type,
        train_number,
        owning_rly,
        coach_status,
        departments,
        vehicle_type,
        workshops,
        sick_heads,
        sort_method,
        order,
        query,
        search_param,
    ):
        # if "both" in coach_status:
        #     actual_coach_status = ["SICKCH", "FITAVL"]
        # else:
        #     actual_coach_status = [coach_status]
        # if "both" in departments:
        #     actual_department = ["MECDFT", "ELCDFT"]
        # else:
        #     actual_department = [departments]
        # if "both" in vehicle_type:
        #     actual_vehicle_type = ["OCV", "PCV"]
        # else:
        #     actual_vehicle_type = [vehicle_type]

        actual_coach_status = coach_status.split("-")
        actual_department = departments.split("-")
        actual_vehicle_type = vehicle_type.split("-")

        sort_method = order + sort_method if order == "-" else sort_method

        result = Data.objects.filter(
            sick_head__in=sick_heads,
            train_number__in=train_number,
            owning_rly__in=owning_rly,
            coach_status__in=actual_coach_status,
            coach_number=complain,
            coach_type__in=coach_type,
            department__in=actual_department,
            vehicle_type__in=actual_vehicle_type,
            workshop__in=workshops,
            problem_date__range=[
                dt.strptime(f"{problem_start} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                dt.strptime(f"{problem_end} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
            ],
        ).order_by(sort_method)

        print("-------------------------------------------------")
        print(f"search_param: {search_param}")
        print(f"query: {query}")
        print("-------------------------------------------------")

        if (search_param != "" or search_param != None) and (
            query != None
        ):
            try:
                query = int(query)
            except:
                query = query.strip()

            # result = result.filter(
            #     Q(id__icontains=query)
            #     | Q(sl_no__icontains=query)
            #     | Q(coach_number__icontains=query)
            #     | Q(train_number__icontains=query)
            #     | Q(owning_rly__icontains=query)
            #     | Q(coach_type__icontains=query)
            #     | Q(coach_status__icontains=query)
            #     | Q(department__icontains=query)
            #     | Q(vehicle_type__icontains=query)
            #     | Q(cause_of_sick_marking__icontains=query)
            #     | Q(workshop__icontains=query)
            #     | Q(sick_head__icontains=query)
            # )

            if search_param == "sl_no":
                if(query == '' or type(query) == str):
                     result = result.filter(Q(sl_no__icontains=query)) 
                     messages.error(request, f"{search_param} should have integer value as input")
                else:
                  result = result.filter(Q(sl_no=query))
            elif search_param == "id":
                 if(query == '' or type(query) == str):
                      messages.error(request,f"{search_param} should have integer value as input")
                      result = result.filter(Q(id__icontains=query))
                 else:
                    result = result.filter(Q(id=query))
            elif search_param == "train_number":
                if(query == '' or  type(query) == str ):
                    result = result.filter(Q(train_number__icontains=query))
                    messages.error(request, f"{search_param} should have integer value as input")
                else:
                    result = result.filter(Q(train_number=query))
            elif search_param == "coach_number":
                if(query == '' or type(query)== str):
                   result = result.filter(Q(coach_number__icontains=query))
                   messages.error(request, f"{search_param} should have integer value as input")
                else:
                    result = result.filter(Q(coach_number=query))
            elif search_param == "owning_rly":
                result = result.filter(Q(owning_rly__icontains=query))
            elif search_param == "coach_type":
                result = result.filter(Q(coach_type__icontains=query))
            elif search_param == "sick_head":
                result = result.filter(Q(sick_head__icontains=query))
            elif search_param == "coach_status":
                result = result.filter(Q(coach_status__icontains=query))
            elif search_param == "department":
                result = result.filter(Q(department__icontains=query))
            elif search_param == "vehicle_type":
                result = result.filter(Q(vehicle_type__icontains=query))
            elif search_param == "workshop":
                result = result.filter(Q(workshop__icontains=query))
            # elif search_param == "":
            #     messages.error(request, "Please select search parameter from dropdown.")
            messages.error(request, f"{query} not found in {search_param}") if (
                len(result) == 0 and query !=""
            )else None
        return result  
        
    def coach_pro_queries(
        request,
        # problem_start,
        # problem_end,
        coach_number_id,
        # coach_type,
        # train_number,
        # owning_rly,
        # coach_status,
        # departments,
        # vehicle_type,
        # workshops,
        # sick_heads,
        sort_method,
        order,
        query,
        search_param,
    ):
        # if "both" in coach_status:
        #     actual_coach_status = ["SICKCH", "FITAVL"]
        # else:
        #     actual_coach_status = [coach_status]
        # if "both" in departments:
        #     actual_department = ["MECDFT", "ELCDFT"]
        # else:
        #     actual_department = [departments]
        # if "both" in vehicle_type:
        #     actual_vehicle_type = ["OCV", "PCV"]
        # else:
        #     actual_vehicle_type = [vehicle_type]

        # sort_method = order + sort_method if order == "-" else sort_method

        result = Data1.objects.filter(
             
            coach_number=coach_number_id,
             
        )

        

        # print("-------------------------------------------------")
        # print(f"search_param: {search_param}")
        # print(f"query: {query}")
        # print("-------------------------------------------------")

        if (search_param != "" or search_param != None) and (
            query != "" or query != None
        ):
            try:
                query = int(query)
            except:
                query = query.strip()

            # result = result.filter(
            #     Q(id__icontains=query)
            #     | Q(sl_no__icontains=query)
            #     | Q(coach_number__icontains=query)
            #     | Q(train_number__icontains=query)
            #     | Q(owning_rly__icontains=query)
            #     | Q(coach_type__icontains=query)
            #     | Q(coach_status__icontains=query)
            #     | Q(department__icontains=query)
            #     | Q(vehicle_type__icontains=query)
            #     | Q(cause_of_sick_marking__icontains=query)
            #     | Q(workshop__icontains=query)
            #     | Q(sick_head__icontains=query)
            # )

            # if search_param == "sl_no":
            #     result = result.filter(Q(sl_no=query))
            # elif search_param == "id":
            #     result = result.filter(Q(id=query))
            # elif search_param == "train_number":
            #     result = result.filter(Q(train_number=query))
            # elif search_param == "coach_number":
            #     result = result.filter(Q(coach_number=query))
            # elif search_param == "owning_rly":
            #     result = result.filter(Q(owning_rly__icontains=query))
            # elif search_param == "coach_type":
            #     result = result.filter(Q(coach_type__icontains=query))
            # elif search_param == "sick_head":
            #     result = result.filter(Q(sick_head__icontains=query))
            # elif search_param == "coach_status":
            #     result = result.filter(Q(coach_status__icontains=query))
            # elif search_param == "department":
            #     result = result.filter(Q(department__icontains=query))
            # elif search_param == "vehicle_type":
            #     result = result.filter(Q(vehicle_type__icontains=query))
            # elif search_param == "workshop":
            #     result = result.filter(Q(workshop__icontains=query))
            # # elif search_param == "":
            # #     messages.error(request, "Please select search parameter from dropdown.")
            # messages.error(request, f"{query} not found in {search_param}") if (
            #     len(result) == 0
            # ) else None

        return result

    def csv_download_query(
        request,
        train_numbers,
        sick_heads,
        owning_rly,
        coach_status,
        department,
        vehicle_type,
        checked_coach_types,
        checked_coach_numbers,
        workshops,
        problem_start,
        problem_end,
    ):
        data = (
            Data.objects.all()
            .values_list(
                "owning_rly",
                "coach_number",
                "coach_type",
                "sick_head",
                "cause_of_sick_marking",
                "reported_defect",
                "work_done",
                "problem_date",
                "placement_date",
                "fit_date",
                "coach_status",
                "department",
                "POH_date",
                "IOH_date",
                "ac_flag",
                "coach_category",
                "vehicle_type",
                "train_number",
                "main_depot",
                "workshop",
                "created_at",
                "created_by",
                "updated_at",
            )
            .filter(
                train_number__in=train_numbers,
                sick_head__in=sick_heads,
                owning_rly__in=owning_rly,
                coach_status__in=coach_status,
                department__in=department,
                vehicle_type__in=vehicle_type,
                coach_type__in=checked_coach_types,
                coach_number__in=checked_coach_numbers,
                workshop__in=workshops,
                problem_date__range=[
                    dt.strptime(f"{problem_start} {START_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                    dt.strptime(f"{problem_end} {END_TIME}", '%Y-%m-%d %H:%M:%S').astimezone(IST),
                ],
            )
        )

    def warranty_complain_graph_query(
        checked_coach_numbers,
        failed_assemblys,
        complaint_ids,
        complain_start, 
        complain_end,
        coach_count,
        sort_method,
    ):
        result_dict = {}
        result = list(
            Data2.objects.filter(
                failed_assembly__in=failed_assemblys,
                complaint_id__in=complaint_ids,
                coach_number__in=checked_coach_numbers,
                complain_date__range=[
                    complain_start,
                    complain_end
                ],
                # placement_date__range=[
                #         f"{placement_start} 00:00:00+00:00",
                #         f"{placement_end} 23:59:00+00:00",
                # ],
                # fit_date__range=[
                #         f"{fit_start} 00:00:00+00:00",
                #         f"{fit_end} 23:59:00+00:00",
                # ],
            ).values_list("coach_number")
        )
        # print(f'result: ', result)
        for r in result:
            if r[0] in result_dict:
                result_dict[r[0]] += 1
            else:
                result_dict[r[0]] = 1

        result = list(result_dict.items())
        result.sort(key=lambda x: x[1], reverse=True)
        table_res = result
        print(result)
        coach_number = []
        count = []
        for r in result:
            if r[0] != None:
                coach_number.append(int(r[0]))
                count.append(r[1])

        if coach_count != "":
            coach_number = coach_number[: int(coach_count)]
            count = count[: int(coach_count)]
            table_res = table_res[: int(coach_count)]

        if sort_method == "asc":
            coach_number.reverse()
            count.reverse()
            table_res.reverse()

        return [coach_number, count, table_res]

    def new_warranty_complain_graph_query(
        checked_coach_numbers,
        failed_assemblys,
        complaint_ids,
        complain_start, 
        complain_end,
        coach_count,
        sort_method,
    ):  
        failed_assembly_data = []
        for i in failed_assemblys:
            if ("\r" in i):
                i = i.replace('\r', '')
            failed_assembly_data.append(i)
        
        result_dict = {}
        result = list(
            Data3.objects.filter(
                failed_assembly__in=failed_assembly_data,
                complaint_id__in=complaint_ids,
                coach_number__in=checked_coach_numbers,
                complain_date__range=[
                    complain_start,
                    complain_end
                ],
                # placement_date__range=[
                #         f"{placement_start} 00:00:00+00:00",
                #         f"{placement_end} 23:59:00+00:00",
                # ],
                # fit_date__range=[
                #         f"{fit_start} 00:00:00+00:00",
                #         f"{fit_end} 23:59:00+00:00",
                # ],
            ).values_list("coach_number")
        )
        # print(f'result: ', result)
        for r in result:
            if r[0] in result_dict:
                result_dict[r[0]] += 1
            else:
                result_dict[r[0]] = 1

        result = list(result_dict.items())
        result.sort(key=lambda x: x[1], reverse=True)
        table_res = result
        print(result)
        coach_number = []
        count = []
        for r in result:
            if r[0] != None:
                coach_number.append(int(r[0]))
                count.append(r[1])

        if coach_count != "":
            coach_number = coach_number[: int(coach_count)]
            count = count[: int(coach_count)]
            table_res = table_res[: int(coach_count)]

        if sort_method == "asc":
            coach_number.reverse()
            count.reverse()
            table_res.reverse()

        return [coach_number, count, table_res]


    def complain_warranty_query(
        request,
        complain,
        failed_assemblys,
        complaint_ids,
        sort_method,
        order,
        query,
        search_param,
        complain_start,
        complain_end
    ):

        sort_method = order + sort_method if order == "-" else sort_method

        result = Data2.objects.filter(
            failed_assembly__in=failed_assemblys,
            complaint_id__in=complaint_ids,
            coach_number=complain,
            complain_date__range=[
                    complain_start,
                    complain_end
                ],

        ).order_by(sort_method)

        print("-------------------------------------------------")
        print(f"search_param: {search_param}")
        print(f"query: {query}")
        print("-------------------------------------------------")

        if (search_param != "" or search_param != None) and (
           query != None
        ):
            try:
                query = int(query)
            except:
                query = query.strip()


            if search_param == "sl_no":
              if(query == "" or type(query) == str):
                result = result.filter(Q(sl_no__icontains=query))
                messages.error(request,f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(sl_no=query))
            elif search_param == "id":
              if(query == "" or type(query)== str ):
                result = result.filter(Q(id__icontains=query))
                messages.error(request,  f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(id=query))
            elif search_param == "complaint_id":
              if(query == "" or type(query) == str):
                result = result.filter(Q(complaint_id__icontains=query))
                messages.error(request,f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(complaint_id=query))
            elif search_param == "coach_number":
              if(query=="" or type(query) == str):
                result = result.filter(Q(coach_number__icontains=query))
                messages.error(request, f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(coach_number=query))
            elif search_param == "failed_assembly":
                result = result.filter(Q(failed_assembly__icontains=query))
            # elif search_param == "":
            #     messages.error(request, "Please select search parameter from dropdown.")
            messages.error(request, f"{query} not found in {search_param}") if (
                len(result) == 0 and query !=""
            ) else None
        return result    
    
    def new_complain_warranty_query(
        request,
        complain,
        failed_assemblys,
        complaint_ids,
        sort_method,
        order,
        query,
        search_param,
        complain_start,
        complain_end
    ):

        sort_method = order + sort_method if order == "-" else sort_method

        result = Data3.objects.filter(
            failed_assembly__in=failed_assemblys,
            complaint_id__in=complaint_ids,
            coach_number=complain,
            complain_date__range=[
                    complain_start,
                    complain_end
                ],
        ).order_by(sort_method)

        print("-------------------------------------------------")
        print(f"search_param: {search_param}")
        print(f"query: {query}")
        print("-------------------------------------------------")

        if (search_param != "" or search_param != None) and (
           query != None
        ):
            try:
                query = int(query)
            except:
                query = query.strip()


            if search_param == "sl_no":
              if(query == "" or type(query) == str):
                result = result.filter(Q(sl_no__icontains=query))
                messages.error(request,f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(sl_no=query))
            elif search_param == "id":
              if(query == "" or type(query)== str ):
                result = result.filter(Q(id__icontains=query))
                messages.error(request,  f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(id=query))
            elif search_param == "complaint_id":
              if(query == "" or type(query) == str):
                result = result.filter(Q(complaint_id__icontains=query))
                messages.error(request,f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(complaint_id=query))
            elif search_param == "coach_number":
              if(query=="" or type(query) == str):
                result = result.filter(Q(coach_number__icontains=query))
                messages.error(request, f"{search_param} should have integer value as input")
              else:
                result = result.filter(Q(coach_number=query))
            elif search_param == "failed_assembly":
                result = result.filter(Q(failed_assembly__icontains=query))
            # elif search_param == "":
            #     messages.error(request, "Please select search parameter from dropdown.")
            messages.error(request, f"{query} not found in {search_param}") if (
                len(result) == 0 and query !=""
            ) else None
        return result    