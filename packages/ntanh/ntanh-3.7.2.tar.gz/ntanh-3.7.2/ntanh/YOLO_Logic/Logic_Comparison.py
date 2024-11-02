def compare_labels(label_list, rule_dict):
    """So sánh list của các nhãn đã predict với dict chuẩn được khái báo trước.
        Lấy label yHat so với y, để đưa ra kết luận OK/NG. Logic như sau:

        -------------------------------------------------------------------------------

        class mParams:
            detect_abnormal_Results_Conclusion = {
                "4": {"Min_num": 0, "Max_num": 1, "name": "Blue"},
                "5": {"Min_num": 0, "Max_num": 1, "name": "White"},
                "6": {"Min_num": 0, "Max_num": 1, "name": "Black"},
                "7": {"Min_num": 0, "Max_num": 0, "name": "No coach"},
                "8": {"Min_num": 0, "Max_num": 0, "name": "Bend"},
                "Sum_same_labels_min_max": {
                    "group1": {"labels": "4,5,6", "min": 0, "max": 1},
                    "group2": {"labels": "3", "min": 0, "max": 1},
                },
            }
            hide_draw_labels = ["3"]

        # Danh sách cần kiểm tra
        list_Need_to_check = [
            [4],  # OK
            [5],  # OK
            [6],  # OK
            [4, 5],  # OK
            [4, 5, 6],  # OK
            [7],  # NG
            [8],  # NG
            [4, 4],  # NG
            [4, 4, 4],  # NG
            [4, 5],  # NG
            [5, 5],  # NG
            [5, 5, 4],  # NG
            [5, 5, 4, 4],  # NG
            [4, 5, 6],  # NG
            [4, 5, 6, 7],  # NG
            [4, 8],  # NG
            [4, 7],  # NG
        ]

        # Thực hiện kiểm tra và in kết quả
        for label1 in list_Need_to_check:
            kq = compare_labels(label1, mParams.detect_abnormal_Results_Conclusion)
            print(label1, kq)

        return:
            f"NG, {'; '.join(violations)}"
            f"OK, {rule_dict[label]['name']}"
        -------------------------------------------------------------------------------

        So sánh nhãn trong `label_list` với quy tắc `Min_num` và `Max_num` từ `rule_dict`.

        Args:
            label_list (list): Danh sách các nhãn cần kiểm tra.
            rule_dict (dict): Từ điển chứa quy tắc kiểm tra các nhãn với:
                - `Min_num`: Số lượng tối thiểu mà nhãn cần phải xuất hiện.
                - `Max_num`: Số lượng tối đa mà nhãn được phép xuất hiện.
                - `name`: Tên của nhãn để hiển thị trong kết quả.

        Returns:
            str: Kết quả kiểm tra theo các trường hợp sau:
                - "OK, name" nếu tất cả các nhãn trong `label_list` thỏa mãn điều kiện Min_num và Max_num.
                - "NG, lý do" nếu có bất kỳ nhãn nào vi phạm các điều kiện:
                    - Số lượng nhãn vượt quá `Max_num`.
                    - Số lượng nhãn ít hơn `Min_num`.
                    - Nhãn yêu cầu xuất hiện ít nhất một lần (Min_num > 0) nhưng không có trong `label_list`.

        Logic:
        - Đầu tiên, đếm số lần xuất hiện của mỗi nhãn trong `label_list`.
        - Đối với mỗi nhãn trong `label_list`, kiểm tra xem số lần xuất hiện có thỏa mãn:
            - Không vượt quá `Max_num`.
            - Không ít hơn `Min_num`.
        - Nếu có nhãn nào yêu cầu số lượng tối thiểu (`Min_num > 0`) nhưng không xuất hiện trong `label_list`,
          thì ghi nhận vi phạm đó.
        - Nếu có bất kỳ vi phạm nào (vượt quá `Max_num`, ít hơn `Min_num` hoặc nhãn bị thiếu), trả về "NG" kèm theo lý do.
        - Nếu tất cả các nhãn đều thỏa mãn, trả về "OK" và tên nhãn đầu tiên trong `label_list`.
    """
    # Đếm số lượng mỗi nhãn xuất hiện trong label_list
    label_count = {}
    for label in label_list:
        str_label = str( label )  # Chuyển label sang chuỗi để khớp với key trong rule_dict
        if str_label in label_count:
            label_count[str_label] += 1
        else:
            label_count[str_label] = 1

    # Danh sách lưu các nhãn vi phạm
    violations = []

    # Kiểm tra từng nhãn dựa trên quy tắc trong rule_dict
    for label, count in label_count.items():
        if label in rule_dict:
            min_num = rule_dict[label].get("Min_num", 0)
            max_num = rule_dict[label]["Max_num"]
            name = rule_dict[label]["name"]

            # Kiểm tra vi phạm Max_num
            if count > max_num:
                if max_num > 0:
                    violations.append(f"{name} > {max_num}")
                else:
                    violations.append(f"{name}")

            # Kiểm tra vi phạm Min_num
            if count < min_num:
                if min_num > 0:
                    violations.append(f"{name} < {min_num}")
                else:
                    violations.append(f"{name}")

    # Kiểm tra các nhãn còn thiếu (Min_num yêu cầu nhưng không có trong danh sách)
    for label, rules in rule_dict.items():
        if label == "Sum_same_labels_min_max":
            continue
        if str(label) not in label_count and rules.get("Min_num", 0) > 0:
            violations.append(f"{rules['name']} < {rules['Min_num']}")

    if "Sum_same_labels_min_max" in rule_dict:
        for grp_key, vl_key in rule_dict["Sum_same_labels_min_max"].items():
            # grp_key="group1"
            # vl_key = {"labels": "7,8", "min": 0, "max": 0}
            gLabels = vl_key["labels"].split(",")
            gmin = vl_key["min"]
            gmax = vl_key["max"]
            predLabels_cnt = 0
            for label, count in label_count.items():
                if label in gLabels:
                    predLabels_cnt += count
            if predLabels_cnt < gmin or predLabels_cnt > gmax:
                violations.append(
                    f"Grp: {vl_key['labels']}: {predLabels_cnt} not in [{gmin},{gmax}]"
                )

    # Nếu có vi phạm, trả về NG và liệt kê lý do
    if violations:
        return f"NG, {'; '.join(violations)}"

    # Nếu không có nhãn nào vi phạm
    # Lấy tên của nhãn đầu tiên trong danh sách label_list
    lbName = "OK, -"
    for label in label_list:
        if label in rule_dict:
            if "name" in rule_dict[label]:
                lbName = f"OK, {rule_dict[label]['name']}"
                break
    return lbName


if __name__ == "__main__":

    class mParams:
        detect_abnormal_Results_Conclusion = {
            "4": {"Min_num": 0, "Max_num": 1, "name": "Blue"},
            "5": {"Min_num": 0, "Max_num": 1, "name": "White"},
            "6": {"Min_num": 0, "Max_num": 1, "name": "Black"},
            "7": {"Min_num": 0, "Max_num": 0, "name": "No coach"},
            "8": {"Min_num": 0, "Max_num": 0, "name": "Bend"},
            "Sum_same_labels_min_max": {
                "group1": {"labels": "4,5,6", "min": 0, "max": 1},
                "group2": {"labels": "3", "min": 0, "max": 1},
            },
        }
        hide_draw_labels = ["3"]

    # Danh sách cần kiểm tra
    list_Need_to_check = [
        [4],  # OK
        [5],  # OK
        [6],  # OK
        [4, 5],  # OK
        [4, 5, 6],  # OK
        [7],  # NG
        [8],  # NG
        [4, 4],  # NG
        [4, 4, 4],  # NG
        [4, 5],  # NG
        [5, 5],  # NG
        [5, 5, 4],  # NG
        [5, 5, 4, 4],  # NG
        [4, 5, 6],  # NG
        [4, 5, 6, 7],  # NG
        [4, 8],  # NG
        [4, 7],  # NG
    ]

    # Thực hiện kiểm tra và in kết quả
    for label1 in list_Need_to_check:
        kq = compare_labels(label1, mParams.detect_abnormal_Results_Conclusion)
        print(label1, kq)
