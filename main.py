import math
import re
import shutil

from pandas import read_excel
from pandas import DataFrame
from matplotlib import pyplot
from PIL import Image


def draw_graph(result_dict_of_probes_intersections, avg_intersections_per_class, distance_to_references_list):
    data_frame_dict = {"x": [], "y": [], "z": []}
    colors = []
    for item in result_dict_of_probes_intersections:
        if list(item.keys())[0] != "unknown":
            if list(item.keys())[0] == "first":
                colors.append("r")
            elif list(item.keys())[0] == "second":
                colors.append("b")
            elif list(item.keys())[0] == "third":
                colors.append("g")
            data_frame_dict["x"].append(list(item.values())[0]["blue"])
            data_frame_dict["y"].append(list(item.values())[0]["violet"])
            data_frame_dict["z"].append(list(item.values())[0]["orange"])
        else:
            print(avg_intersections_per_class)
            for i in range(0, len(avg_intersections_per_class) - 1):
                colors.append("y")
            colors.append("c")
    for item in avg_intersections_per_class:
        data_frame_dict["x"].append(list(item.values())[0]["blue"])
        data_frame_dict["y"].append(list(item.values())[0]["violet"])
        data_frame_dict["z"].append(list(item.values())[0]["orange"])

    # colors = ['r', 'r', 'r', 'r', 'r', 'b', 'b', 'b', 'b', 'b', 'g', 'g', 'g', 'g', 'g', 'y', 'y', 'y', 'c']

    print(colors)
    print(data_frame_dict)

    data = DataFrame(data_frame_dict)
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(data['x'], data['y'], data['z'], c=colors)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    if get_class_type(distance_to_references_list) == "first":
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-2]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-2]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-2]],
            linewidth=4,
            c='b'
        )
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-3]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-3]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-3]],
            c='b'
        )
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-4]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-4]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-4]],
            c='b'
        )
    elif get_class_type(distance_to_references_list) == "second":
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-2]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-2]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-2]],
            c='b'
        )
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-3]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-3]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-3]],
            linewidth=4,
            c='b'
        )
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-4]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-4]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-4]],
            c='b'
        )
    elif get_class_type(distance_to_references_list) == "third":
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-2]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-2]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-2]],
            c='b'
        )
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-3]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-3]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-3]],
            c='b'
        )
        ax.plot(
            [data_frame_dict["x"][-1], data_frame_dict["x"][-4]],
            [data_frame_dict["y"][-1], data_frame_dict["y"][-4]],
            [data_frame_dict["z"][-1], data_frame_dict["z"][-4]],
            linewidth=4,
            c='b'
        )
    ax.view_init(elev=30, azim=270)
    pyplot.show()


def read_image(image_path):
    pixel_rgb_values_list = []
    with open(image_path, "rb") as unknown_image:
        pixel_data = Image.open(unknown_image).convert("RGB").getdata()
        for pixel in pixel_data:
            pixel_rgb_values_list.append(pixel)

    return pixel_rgb_values_list


def read_all_recognized_images(path_to_excel):
    file = read_excel(path_to_excel)
    list_of_paths = list(file["path"])
    counter_first, counter_second, counter_third = 0, 0, 0
    pixel_rgb_values_per_class = []
    for path in list_of_paths:
        if str(path).find("first") != -1:
            counter_first += 1
            pixel_rgb_values_per_class.append(read_image(path))
        elif str(path).find("second") != -1:
            counter_second += 1
            pixel_rgb_values_per_class.append(read_image(path))
        elif str(path).find("third") != -1:
            counter_third += 1
            pixel_rgb_values_per_class.append(read_image(path))
    return pixel_rgb_values_per_class


def get_class_type(distance_to_references_list):
    if distance_to_references_list.index(min(distance_to_references_list)) == 0:
        return "first"
    elif distance_to_references_list.index(min(distance_to_references_list)) == 1:
        return "second"
    elif distance_to_references_list.index(min(distance_to_references_list)) == 2:
        return "third"


def fill_excel_number_and_class_columns(excel_path):
    file = read_excel(excel_path)
    list_of_paths = list(file["path"])
    list_of_search_results = []
    numbers_for_n_col = []
    types_for_class_col = []
    for path in list_of_paths:
        list_of_search_results.append(re.search("/([fFsStTUu])(.+\\d+)", path).group())
    print(list_of_search_results)
    for search_result in list_of_search_results:
        types_for_class_col.append(re.search("[a-zA-Z]+", search_result)[0])
        numbers_for_n_col.append(re.search("[0-9]+", search_result)[0])
    for i in range(0, len(numbers_for_n_col)):
        file.at[i, "n"] = numbers_for_n_col[i]
        file.at[i, "class"] = types_for_class_col[i]
    file.to_excel(excel_path, index=False)


def copy_file_to_recognized(path_to_file, path_to_move):
    shutil.move(path_to_file, path_to_move)


def draw_probes_for_image(image_path):
    regex_results_list = get_regex_number_and_name_out_of_path(image_path)
    with open(image_path, "rb") as unknown_image:
        image = Image.open(unknown_image).convert("RGB")
        pixels = image.load()
        draw_probe_vertical(image, pixels, (0, 128, 255), 15)
        draw_probe_vertical(image, pixels, (64, 0, 255), 11)
        draw_probe_horizontal(image, pixels, (255, 128, 64), 16)
        image.save(f"images/images_with_probes/{regex_results_list[0][0]}{regex_results_list[1][0]}.png", format="PNG")


def draw_probe_vertical(image, image_pixels, rgb_color_tuple, i_value):
    for j in range(image.size[1]):
        if image_pixels[i_value, j] != (0, 0, 0):
            image_pixels[i_value, j] = rgb_color_tuple


def draw_probe_horizontal(image, image_pixels, rgb_color_tuple, j_value):
    for i in range(image.size[1]):
        if image_pixels[i, j_value] != (0, 0, 0):
            image_pixels[i, j_value] = rgb_color_tuple


def get_regex_number_and_name_out_of_path(image_path):
    list_to_return = []
    list_of_search_results = []
    numbers_for_n_col = []
    types_for_class_col = []
    list_of_search_results.append(re.search("/([fFsStTUu])(.+\\d+)", image_path).group())
    for search_result in list_of_search_results:
        types_for_class_col.append(re.search("[a-zA-Z]+", search_result)[0])
        numbers_for_n_col.append(re.search("[0-9]+", search_result)[0])
    list_to_return.append(types_for_class_col)
    list_to_return.append(numbers_for_n_col)

    return list_to_return


def get_probes_intersections(image_path):
    result_dict = {}
    dict_of_intersections = {}
    regex_results_list = get_regex_number_and_name_out_of_path(image_path)
    image_with_probes_path = f"images/images_with_probes/{regex_results_list[0][0]}{regex_results_list[1][0]}.png"
    blue_probe_intersection_counter, violet_probe_intersection_counter, orange_probe_intersection_counter = 0, 0, 0
    with open(image_with_probes_path, "rb") as unknown_image:
        image = Image.open(unknown_image).convert("RGB")
        pixels = image.load()
        for j in range(image.size[1]):
            if pixels[15, j] == (0, 0, 0) and pixels[15, j + 1] != (0, 0, 0):
                blue_probe_intersection_counter += 1
            if pixels[11, j] == (0, 0, 0) and pixels[11, j + 1] != (0, 0, 0):
                violet_probe_intersection_counter += 1
        for i in range(image.size[0]):
            if pixels[i, 16] == (0, 0, 0) and pixels[i + 1, 16] != (0, 0, 0):
                orange_probe_intersection_counter += 1
        dict_of_intersections["blue"] = blue_probe_intersection_counter
        dict_of_intersections["violet"] = violet_probe_intersection_counter
        dict_of_intersections["orange"] = orange_probe_intersection_counter
        result_dict[regex_results_list[0][0]] = dict_of_intersections
    return result_dict


def read_all_images_intersections(list_of_paths):
    all_images_intersections_list = []
    for image_path in list_of_paths:
        all_images_intersections_list.append(get_probes_intersections(image_path))
    print(all_images_intersections_list)
    return all_images_intersections_list


def find_avg_intersections_for_each_class(all_images_intersections_list):
    avg_intersections_per_class = [
        {"first": {"blue": 0, "violet": 0, "orange": 0}},
        {"second": {"blue": 0, "violet": 0, "orange": 0}},
        {"third": {"blue": 0, "violet": 0, "orange": 0}},
        {"unknown": {"blue": 0, "violet": 0, "orange": 0}}
    ]
    first_class_counter, second_class_counter, third_class_counter = 0, 0, 0
    for dictionary in all_images_intersections_list:
        key = list(dictionary.keys())[0]
        value = list(dictionary.values())[0]
        if key == "first":
            first_class_counter += 1
            avg_intersections_per_class[0][key]["blue"] = (avg_intersections_per_class[0][key]["blue"]
                                                           + value["blue"])
            avg_intersections_per_class[0][key]["violet"] = (avg_intersections_per_class[0][key]["violet"]
                                                             + value["violet"])
            avg_intersections_per_class[0][key]["orange"] = (avg_intersections_per_class[0][key]["orange"]
                                                             + value["orange"])
        elif key == "second":
            second_class_counter += 1
            avg_intersections_per_class[1][key]["blue"] = (avg_intersections_per_class[1][key]["blue"]
                                                           + value["blue"])
            avg_intersections_per_class[1][key]["violet"] = (avg_intersections_per_class[1][key]["violet"]
                                                             + value["violet"])
            avg_intersections_per_class[1][key]["orange"] = (avg_intersections_per_class[1][key]["orange"]
                                                             + value["orange"])
        elif key == "third":
            third_class_counter += 1
            avg_intersections_per_class[2][key]["blue"] = (avg_intersections_per_class[2][key]["blue"]
                                                           + value["blue"])
            avg_intersections_per_class[2][key]["violet"] = (avg_intersections_per_class[2][key]["violet"]
                                                             + value["violet"])
            avg_intersections_per_class[2][key]["orange"] = (avg_intersections_per_class[2][key]["orange"]
                                                             + value["orange"])
        elif key == "unknown":
            avg_intersections_per_class[3][key]["blue"] = (avg_intersections_per_class[3][key]["blue"]
                                                           + value["blue"])
            avg_intersections_per_class[3][key]["violet"] = (avg_intersections_per_class[3][key]["violet"]
                                                             + value["violet"])
            avg_intersections_per_class[3][key]["orange"] = (avg_intersections_per_class[3][key]["orange"]
                                                             + value["orange"])
    avg_intersections_per_class[0]["first"]["blue"] = (avg_intersections_per_class[0]["first"]["blue"]
                                                       // first_class_counter)
    avg_intersections_per_class[0]["first"]["violet"] = (avg_intersections_per_class[0]["first"]["violet"]
                                                         // first_class_counter)
    avg_intersections_per_class[0]["first"]["orange"] = (avg_intersections_per_class[0]["first"]["orange"]
                                                         // first_class_counter)

    avg_intersections_per_class[1]["second"]["blue"] = (avg_intersections_per_class[1]["second"]["blue"]
                                                        // second_class_counter)
    avg_intersections_per_class[1]["second"]["violet"] = (avg_intersections_per_class[1]["second"]["violet"]
                                                          // second_class_counter)
    avg_intersections_per_class[1]["second"]["orange"] = (avg_intersections_per_class[1]["second"]["orange"]
                                                          // second_class_counter)

    avg_intersections_per_class[2]["third"]["blue"] = (avg_intersections_per_class[2]["third"]["blue"]
                                                       // third_class_counter)
    avg_intersections_per_class[2]["third"]["violet"] = (avg_intersections_per_class[2]["third"]["violet"]
                                                         // third_class_counter)
    avg_intersections_per_class[2]["third"]["orange"] = (avg_intersections_per_class[2]["third"]["orange"]
                                                         // third_class_counter)

    return avg_intersections_per_class


def get_distance_list_to_each_reference(avg_intersections_per_class):
    distance_to_references_list = []
    print(avg_intersections_per_class)
    unknown_class_values = avg_intersections_per_class[3]["unknown"]
    distance_to_references_list.append(
        math.sqrt((avg_intersections_per_class[0]["first"]["blue"] - unknown_class_values["blue"]) ** 2
                  + (avg_intersections_per_class[0]["first"]["violet"] - unknown_class_values["violet"]) ** 2
                  + (avg_intersections_per_class[0]["first"]["orange"] - unknown_class_values["orange"]) ** 2)
    )
    distance_to_references_list.append(
        math.sqrt((avg_intersections_per_class[1]["second"]["blue"] - unknown_class_values["blue"]) ** 2
                  + (avg_intersections_per_class[1]["second"]["violet"] - unknown_class_values["violet"]) ** 2
                  + (avg_intersections_per_class[1]["second"]["orange"] - unknown_class_values["orange"]) ** 2)
    )
    distance_to_references_list.append(
        math.sqrt((avg_intersections_per_class[2]["third"]["blue"] - unknown_class_values["blue"]) ** 2
                  + (avg_intersections_per_class[2]["third"]["violet"] - unknown_class_values["violet"]) ** 2
                  + (avg_intersections_per_class[2]["third"]["orange"] - unknown_class_values["orange"]) ** 2)
    )

    return distance_to_references_list


def recognize_in_excel(path_to_excel, class_type, distances_to_references):
    file = read_excel(path_to_excel)
    file.at[file.index[-1], "class"] = class_type
    for i in range(0, len(distances_to_references)):
        file.at[file.index[i], "distance"] = distances_to_references[i]
    if path_to_excel == "data_images.xlsx":
        copy_file_to_recognized(
            file.at[file.index[-1], "path"], "images/recognized/" + class_type + str(len(list(file["path"]))) + ".png"
        )
        file.at[file.index[-1], "path"] = "images/recognized/" + class_type + str(len(list(file["path"]))) + ".png"
    file.to_excel(path_to_excel, index=False)


def fill_z1_z2_z3_excel(excel_path, all_images_intersections_list):
    file = read_excel(excel_path)
    counter = 0
    for intersection_dict in all_images_intersections_list:
        print(list(intersection_dict.values())[0]["blue"])
        file.at[counter, "z1"] = list(intersection_dict.values())[0]["blue"]
        file.at[counter, "z2"] = list(intersection_dict.values())[0]["violet"]
        file.at[counter, "z3"] = list(intersection_dict.values())[0]["orange"]
        counter += 1
    file.to_excel(excel_path, index=False)


if __name__ == '__main__':
    excel_file = read_excel("data_images.xlsx")
    paths_list = list(excel_file["path"])
    # draw_graph("data.xlsx")

    fill_excel_number_and_class_columns("data_images.xlsx")
    read_all_recognized_images("data_images.xlsx")

    for path in paths_list:
        draw_probes_for_image(path)

    draw_graph(
        read_all_images_intersections(paths_list),
        find_avg_intersections_for_each_class(read_all_images_intersections(paths_list)),
        get_distance_list_to_each_reference(find_avg_intersections_for_each_class(read_all_images_intersections(paths_list)))
    )

    recognize_in_excel(
        "data_images.xlsx",
        get_class_type(
            get_distance_list_to_each_reference(
                find_avg_intersections_for_each_class(read_all_images_intersections(paths_list))
            )
        ),
        get_distance_list_to_each_reference(
            find_avg_intersections_for_each_class(read_all_images_intersections(paths_list))
        )
    )
    fill_z1_z2_z3_excel("data_images.xlsx", read_all_images_intersections(paths_list))
