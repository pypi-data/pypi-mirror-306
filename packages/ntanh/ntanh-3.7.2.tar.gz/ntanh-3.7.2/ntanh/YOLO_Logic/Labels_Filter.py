from collections import deque
def test():
    print("Test, Labels_Filter at:", __file__)

# ==========================================================================================

class LabelFilter_1day_so:
    def __init__(self, min_consecutive):
        self.min_consecutive = min_consecutive
        self.buffer = deque(maxlen=min_consecutive)
        self.valid_values = deque(maxlen=min_consecutive)
        self.result = deque(maxlen=min_consecutive)

    def process_value(self, value):
        self.buffer.append(value)
        if len(self.buffer) == self.min_consecutive and len(set(self.buffer)) == 1:
            self.valid_values.append(value)
        if value in set(self.valid_values):
            self.result.append(value)
        if len(self.result) > 0:
            return self.result[-1]
        return []

# ==========================================================================================

class clsLabelFilter_list_bboxes:
    def __init__(self, min_consecutive):
        self.min_consecutive = min_consecutive
        self.buffer = deque(maxlen=min_consecutive)  # Lưu trữ các frame gần nhất
        self.valid_values = deque( maxlen=min_consecutive )  # Lưu trữ kết quả hợp lệ gần nhất
        self.result = None  # Kết quả ổn định gần nhất

    def process_value(self, value, debug=False):
        label_ids = tuple( sorted([item[0] for item in value]) )  # Lấy danh sách các label_id và sắp xếp
        self.buffer.append(label_ids)  # Thêm danh sách label_id vào buffer
        if debug:
            for ids in self.buffer:
                print(self.buffer[0], '==', ids )
        # Kiểm tra xem có đủ frame trong buffer và tất cả frame đều có cùng số lượng label_id hay không
        if len(self.buffer) == self.min_consecutive and all( self.buffer[0] == ids for ids in self.buffer ):
            self.valid_values.append(value)  # Nếu đúng thì cập nhật valid_values
            self.result = value  # Cập nhật kết quả ổn định gần nhất

        # Nếu có kết quả hợp lệ, trả về kết quả ổn định gần nhất
        if self.result:
            return self.result
        return []  # Nếu không có kết quả hợp lệ, trả về rỗng

# ==========================================================================================

class clsFilter_Frames_sep_by_labels:
    """
    Filter bbox trong frames: [(2, 4, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (3, 0.52, 0.51, 0.2, 0.2)]
    Chương trình sẽ tách các labels ra, và fileter theo từng nhóm labels đó, cùng labels vào 1 nhóm, có windows riêng cho mỗi label
    Cách dùng:
        class Param:
            def __init__(self, ):
                self.ClassNames = {
                    0: "Blue Hat",
                    1: "W Hat",
                    2: "Black Hat",
                    3: "Person",
                    4: "Blue",
                    5: "White",
                    6: "Black",
                    7: "No Shirt",
                    8: "Bend",
                }
                self.remove_outliers_online_windows_len_by_class_name = {
                    "default": 3,
                    0: 2,
                    1: 2,
                    2: 4,
                    3: 2,
                    4: 2,
                    5: 2,
                    6: 2,
                    7: 2,
                    8: 1,
                }
        mParams=Param()
        mFilter_Frames = Filter_Frames_sep_by_labels(ClassNames=mParams.ClassNames, windows_len_by_class=mParams.remove_outliers_online_windows_len_by_class_name)
        for cnt,frame1 in enumerate(frame): # Lặp qua các lần predict khác nhau.
            print(cnt, ">", frame1)
            vl=mFilter_Frames.Update(frame1, stt=cnt)
            print(cnt,'-', vl)
            print()
    """
    def __init__(self, ClassNames, windows_len_by_class):
        self.FilLabel={}
        self.ThisTime_bbox = {}
        self.ClassName = ClassNames
        for key, val in ClassNames.items(): 
            if key in windows_len_by_class.keys():
                thisWindow = windows_len_by_class[key]
            else:
                thisWindow = windows_len_by_class["default"]

            self.FilLabel[key]=clsLabelFilter_list_bboxes(min_consecutive=thisWindow)
            self.ThisTime_bbox [key]=[]
        self.Saved_thistime=self.ThisTime_bbox.copy()

    def ThisTime_bbox_clear(self):
        self.ThisTime_bbox=self.Saved_thistime.copy()

    def Update(self, frameBoxes, stt=None, debug=False):
        if debug:
            print()            
            print(stt, ":", frameBoxes)

        self.ThisTime_bbox_clear()
        labels = set([bbox[0] for bbox in frameBoxes]) #[(2, 0, 0.1, 0.2, 0.2), (2, 0.5, 0.5, 0.2, 0.2)]
        for label1 in labels:
            mBBox = []
            for bbox in frameBoxes:
                label_id, x, y, w, h = bbox
                if label_id == label1:
                    mBBox.append(bbox)
            self.ThisTime_bbox[label1]= mBBox

        # Filter this frame
        ret=[]
        for label_id, frame in self.ThisTime_bbox.items():
            # if frame:
            #     print(label_id, ":" * label_id, frame)
            vl = self.FilLabel[label_id].process_value(frame)
            ret.extend(vl)
            if debug: print(label_id, ":" * label_id, vl)
        return ret


# ==========================================================================================
def tim_so_dong_nhat(my_set):
    # Chuyển set thành list để có thể đếm số lần xuất hiện
    my_list = list(my_set)

    # Sử dụng từ điển để đếm tần suất
    so_lan_xuat_hien = {}
    for x in my_list:
        if x in so_lan_xuat_hien:
            so_lan_xuat_hien[x] += 1
        else:
            so_lan_xuat_hien[x] = 1

    # Tìm phần tử có số lần xuất hiện nhiều nhất
    gia_tri_lon_nhat = max(so_lan_xuat_hien.values())
    for k, v in so_lan_xuat_hien.items():
        if v == gia_tri_lon_nhat:
            return k

# # Ví dụ sử dụng:
# my_set = {1, 2, 3, 2, 4, 2, 5}
# ket_qua = tim_so_dong_nhat(my_set)
# print(f"Số xuất hiện nhiều nhất là: {ket_qua}")
# ==========================================================================================

def getframe1_keys(bboxes):
    """
    bboxes=[(22, 0, 0.1, 0.2, 0.2), (33, 0.5, 0.5, 0.2, 0.2)]
    ret   ='22,33'
    """
    thisF=[]
    for x in bboxes: 
        thisF.append(str(x[0])) 
    thisF.sort()
    ret=','.join(thisF)
    return ret


def GetSet_From_deque(mDeque):
    """
    mDeque=[(22, 0, 0.1, 0.2, 0.2), (33, 0.5, 0.5, 0.2, 0.2)], [(44, 1, 0.12, 0.21, 0.21), (55, 0.5, 0.5, 0.2, 0.2)]
    ret={'22,33','44,55'}
    """
    mDeque_values_keys=[]
    for frame1 in list(mDeque):
        thisF=getframe1_keys(bboxes=frame1)
        mDeque_values_keys.append(thisF)
    return set(mDeque_values_keys)

def fnRemove_outliers_online(min_consecutive=3):    
    buffer = deque(maxlen=min_consecutive*2)
    valid_values = deque(maxlen=min_consecutive)
    result=['']

    def process_value(value):        
        N=0
        if len(buffer) > 0:
            N = len([x[0] for x in buffer[-1]])
        buffer.append(value)        
        buffer_values_keys = GetSet_From_deque(buffer)
        # print('buffer_values_keys:', buffer_values_keys)
        if len(buffer) == min_consecutive and len(buffer_values_keys) == 1:
            valid_values.append(value)

        valid_values_keys = GetSet_From_deque( valid_values)
        # print("valid_values_keys:", valid_values_keys)

        thisf=getframe1_keys(value)
        if thisf in valid_values_keys:
            result[0]=value
        return result[0]

    return process_value


if __name__ == "__main__":

    # Sample frames with (label_id, x, y, w, h)
    if 1:
        frame=[]
        frame.append( [(2, 0, 0.1, 0.2, 0.2), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 1, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 2, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 3, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 4, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2)])
        frame.append( [(3, 5, 0.1, 0.2, 0.2),(3, 5, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2)])
        frame.append( [(2, 6, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2)])
        frame.append( [(2, 7, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2)])
        frame.append( [(2, 8, 0.1, 0.2, 0.2)] )
        frame.append( [(2, 9, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.52, 0.52, 0.2, 0.2)])
        frame.append( [(2, 10, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.54, 0.51, 0.2, 0.2)])
        frame.append( [(2, 11, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.54, 0.51, 0.2, 0.2), (2, 0.54, 0.51, 0.2, 0.2)])
        frame.append( [(2, 12, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.56, 0.53, 0.2, 0.2)])
        frame.append( [(2, 13, 0.1, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2), (2, 0.52, 0.51, 0.2, 0.2)])
        frame.append([(4, 14, 0.12, 0.21, 0.21), (2, 14, 0.12, 0.21, 0.21), (4, 14, 0.12, 0.21, 0.21), (5, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(4, 14, 0.12, 0.21, 0.21), (2, 14, 0.12, 0.21, 0.21), (4, 14, 0.12, 0.21, 0.21), (5, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(4, 14, 0.12, 0.21, 0.21), (2, 14, 0.12, 0.21, 0.21), (4, 14, 0.12, 0.21, 0.21), (5, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(4, 14, 0.12, 0.21, 0.21), (2, 14, 0.12, 0.21, 0.21), (4, 14, 0.12, 0.21, 0.21), (5, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(4, 14, 0.12, 0.21, 0.21), (2, 14, 0.12, 0.21, 0.21), (4, 14, 0.12, 0.21, 0.21), (5, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(4, 14, 0.12, 0.21, 0.21), (2, 14, 0.12, 0.21, 0.21), (4, 14, 0.12, 0.21, 0.21), (5, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 15, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 16, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [])
        frame.append( [(2, 17, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 18, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 19, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 20, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append( [(2, 21, 0.51, 0.2, 0.2)])
        frame.append( [(2, 22, 0.52, 0.21, 0.21)])
        frame.append( [(2, 23, 0.52, 0.21, 0.21)])
        frame.append( [(2, 24, 0.52, 0.21, 0.21)])
        frame.append([(2, 17, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(2, 18, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(2, 19, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(2, 19, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(2, 190, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(2, 20, 0.12, 0.21, 0.21), (2, 0.5, 0.5, 0.2, 0.2)])
        frame.append([(2, 21, 0.51, 0.2, 0.2)])
        frame.append([(2, 22, 0.52, 0.21, 0.21)])
        frame.append([(2, 23, 0.52, 0.21, 0.21)])
        frame.append([(2, 24, 0.52, 0.21, 0.21)])

    RUN=3
    if RUN==1:
        # Filter các bboxes, khác nhau về nhãn và số lượng đều được, nhưng không fileter độ dài window theo từng nhãn
        mFilter=fnRemove_outliers_online()
        for cnt,frame1 in enumerate(frame):
            print(cnt, frame1 )
            vl=mFilter(frame1)
            print(cnt, vl )
            print()

    if RUN==2:
        mLabelFilter = clsLabelFilter_list_bboxes(3)

        for cnt,frame1 in enumerate(frame):
            vl = mLabelFilter.process_value(frame1)
            print(cnt, frame1 )
            print(cnt, vl )
            print()
    if RUN==3:
        class Param:
            def __init__(self, ):
                self.ClassNames = {
                    0: "Blue Hat",
                    1: "W Hat",
                    2: "Black Hat",
                    3: "Person",
                    4: "Blue",
                    5: "White",
                    6: "Black",
                    7: "No Shirt",
                    8: "Bend",
                }
                self.remove_outliers_online_windows_len_by_class_name = {
                    "default": 3,
                    0: 2,
                    1: 2,
                    2: 4,
                    3: 2,
                    4: 2,
                    5: 2,
                    6: 2,
                    7: 2,
                    8: 1,
                }
        mParams=Param()
        # Filter các bboxes, khác nhau về nhãn và số lượng đều được, có fileter độ dài window theo từng nhãn
        mFilter_Frames = clsFilter_Frames_sep_by_labels(ClassNames=mParams.ClassNames, windows_len_by_class=mParams.remove_outliers_online_windows_len_by_class_name)
        for cnt,frame1 in enumerate(frame):
            print(cnt, ">", frame1)
            bboxes_out=mFilter_Frames.Update(frame1, stt=cnt)
            print(cnt,'-', bboxes_out)
            print()
