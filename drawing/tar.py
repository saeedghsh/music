"""Some drawing utils"""
import os
import cv2

from core.notation import Note, FrequencyComputer


INSTRUMENTS = {
    "tar": {
        "small_image": {
            "path": "images/tar_small_1290x362.jpg",
            "fret_position_row_27_fret": {
                0: 162,
                1: 206,
                2: 230,
                3: 255,
                4: 295,
                5: 313,
                6: 333,
                7: 372,
                8: 398,
                9: 424,
                10: 448,
                11: 476,
                12: 494,
                13: 513,
                14: 540,
                15: 553,
                16: 568,
                17: 599,
                18: 618,
                19: 625,
                20: 638,
                21: 666,
                22: 679,
                23: 695,
                24: 716,
                25: 734,
                26: 752,
                27: 767,
            },
            "fret_position_col": {
                "min": 150,
                "max": 208,
            },
        },
        "large_image": {"path": "images/tar_large_3910x1097.jpg"},
    }
}


def draw_tar_notes_and_frequencies(string_notes: list, save_to_file: bool = True):
    # pylint: disable=missing-function-docstring
    # pylint: disable=no-member
    # pylint: disable=too-many-locals
    if len(string_notes) != 28:
        raise NotImplementedError(
            "Curretnly only 27-fret count (28 including open-hand) is supported."
        )

    col_min = INSTRUMENTS["tar"]["small_image"]["fret_position_col"]["min"]
    col_max = INSTRUMENTS["tar"]["small_image"]["fret_position_col"]["max"]
    extend_fret_to_right = 0
    horizonal_distance_text_to_fret_line = 20

    color = (20, 20, 245)

    line_thickness = 2
    line_color = color

    fret_number_scale = 0.5
    fret_number_color = color
    fret_number_thickness = 2

    note_scale = 0.5
    note_color = color
    note_thickness = 1

    tar_small = INSTRUMENTS["tar"]["small_image"]["path"]
    img = cv2.imread(tar_small)
    fret_position_row = INSTRUMENTS["tar"]["small_image"]["fret_position_row_27_fret"]
    for fret_number, row in fret_position_row.items():
        fret_line_start_point = (col_min, row)
        fret_line_end_point = (col_max + extend_fret_to_right, row)

        fret_number_origin = (col_min - horizonal_distance_text_to_fret_line, row)
        note_origin = (col_max + extend_fret_to_right + 20, row)

        cv2.line(
            img, fret_line_start_point, fret_line_end_point, line_color, line_thickness
        )

        # Fret number
        cv2.putText(
            img,
            str(fret_number),
            fret_number_origin,
            cv2.FONT_HERSHEY_SIMPLEX,
            fret_number_scale,
            fret_number_color,
            fret_number_thickness,
        )

        note_name = string_notes[fret_number]
        letter, accidental, octave = Note.decompose_name(note_name)
        frequency = FrequencyComputer.compute_frequency(letter, accidental, octave)

        cv2.putText(
            img,
            f"{note_name} {frequency:.2f} Hz",
            note_origin,
            cv2.FONT_HERSHEY_SIMPLEX,
            note_scale,
            note_color,
            note_thickness,
        )

    if save_to_file:
        dir_path, filename = os.path.split(tar_small)
        base_name, ext = os.path.splitext(filename)
        new_base_name = base_name + "_string_annotated"
        output_path = os.path.join(dir_path, new_base_name + ext)
        cv2.imwrite(output_path, img)

    # Set window name
    window_name = "Image"
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()