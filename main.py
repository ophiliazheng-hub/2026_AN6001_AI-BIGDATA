import asyncio

import flet as ft


STARTING_VALUES = [5, 3, 8, 1, 4]
PASTELS = [
    ft.Colors.PINK_200,
    ft.Colors.LIGHT_BLUE_200,
    ft.Colors.YELLOW_200,
    ft.Colors.LIGHT_GREEN_200,
    ft.Colors.PURPLE_200,
]


def main(page: ft.Page):
    page.title = "Bubble Sort Studio"
    page.bgcolor = ft.Colors.PINK_50
    page.padding = 20
    page.spacing = 0
    page.scroll = ft.ScrollMode.AUTO

    values = STARTING_VALUES.copy()
    pass_number = 0
    compare_index = 0
    comparisons = 0
    swaps = 0
    swaps_this_pass = 0
    finished = False
    bubble_run_id = 0

    async def float_bubbles(pair_index, run_id):
        starts = [pair_index * 56 + offset for offset in (8, 34, 62, 88)]
        for bubble, x in zip(bubbles, starts):
            bubble.left = x
            bubble.top = 78
            bubble.opacity = 0
        page.update()
        await asyncio.sleep(0.03)

        end_positions = [10, 1, 20, 8]
        for bubble, x, y in zip(bubbles, starts, end_positions):
            bubble.left = x + (4 if y % 2 else -3)
            bubble.top = y
            bubble.opacity = 0.88
        page.update()

        await asyncio.sleep(0.82)
        if run_id == bubble_run_id:
            for bubble in bubbles:
                bubble.top = 78
                bubble.opacity = 0
            page.update()

    def trigger_bubbles(pair_index):
        nonlocal bubble_run_id
        bubble_run_id += 1
        asyncio.create_task(float_bubbles(pair_index, bubble_run_id))

    def refresh():
        for index, value in enumerate(values):
            tile_labels[index].value = str(value)
            is_active = not finished and index in (compare_index, compare_index + 1)
            tile_boxes[index].bgcolor = ft.Colors.ORANGE_200 if is_active else PASTELS[index]
            tile_boxes[index].border = ft.Border.all(3 if is_active else 2, ft.Colors.WHITE)
            tile_boxes[index].shadow = ft.BoxShadow(
                blur_radius=12 if is_active else 8,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.24, ft.Colors.PINK_700),
                offset=ft.Offset(0, 4),
            )

        if finished:
            status_text.value = "Sorted! Every neighboring pair is now in ascending order."
        else:
            status_text.value = (
                f"Pass {pass_number + 1} · Comparing positions "
                f"{compare_index + 1} and {compare_index + 2}"
            )
        stats_text.value = f"Comparisons: {comparisons}   ·   Swaps: {swaps}"
        next_button.disabled = finished
        page.update()

    def reset():
        nonlocal values, pass_number, compare_index, comparisons, swaps
        nonlocal swaps_this_pass, finished, bubble_run_id
        values = STARTING_VALUES.copy()
        pass_number = 0
        compare_index = 0
        comparisons = 0
        swaps = 0
        swaps_this_pass = 0
        finished = False
        bubble_run_id += 1
        for bubble in bubbles:
            bubble.top = 78
            bubble.opacity = 0
        quiz_feedback.value = ""
        refresh()

    def advance():
        nonlocal pass_number, compare_index, comparisons, swaps
        nonlocal swaps_this_pass, finished
        if finished:
            return

        current_pair = compare_index
        trigger_bubbles(current_pair)
        left, right = current_pair, current_pair + 1
        comparisons += 1
        if values[left] > values[right]:
            values[left], values[right] = values[right], values[left]
            swaps += 1
            swaps_this_pass += 1

        compare_index += 1
        if compare_index >= len(values) - 1 - pass_number:
            if swaps_this_pass == 0 or pass_number >= len(values) - 2:
                finished = True
            else:
                pass_number += 1
                compare_index = 0
                swaps_this_pass = 0
        refresh()

    def answer_quiz(should_swap):
        if should_swap:
            quiz_feedback.value = (
                "That's right! Swap them so the larger value moves toward the right."
            )
        else:
            quiz_feedback.value = (
                "Try again: for ascending order, swap when the left value is larger."
            )
        page.update()

    def section(title, description, color, content):
        return ft.Container(
            expand=True,
            padding=18,
            border_radius=20,
            bgcolor=color,
            content=ft.Column(
                tight=True,
                spacing=10,
                controls=[
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                    ft.Text(description, color=ft.Colors.GREY_800),
                    content,
                ],
            ),
        )

    tile_boxes = []
    tile_labels = []
    for index, value in enumerate(values):
        label = ft.Text(str(value), size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900)
        box = ft.Container(
            width=60,
            height=60,
            border_radius=30,
            border=ft.Border.all(2, ft.Colors.WHITE),
            bgcolor=PASTELS[index],
            shadow=ft.BoxShadow(
                blur_radius=8,
                spread_radius=1,
                color=ft.Colors.with_opacity(0.24, ft.Colors.PINK_700),
                offset=ft.Offset(0, 4),
            ),
            content=ft.Stack(
                alignment=ft.Alignment.CENTER,
                controls=[
                    label,
                    ft.Container(
                        left=12,
                        top=9,
                        width=13,
                        height=6,
                        border_radius=8,
                        bgcolor=ft.Colors.WHITE,
                        opacity=0.78,
                    ),
                ],
            ),
        )
        tile_labels.append(label)
        tile_boxes.append(box)

    bubbles = [
        ft.Container(
            left=0,
            top=78,
            width=size,
            height=size,
            opacity=0,
            bgcolor=color,
            border=ft.Border.all(2, ft.Colors.WHITE),
            border_radius=20,
            animate_position=ft.Animation(duration=720, curve=ft.AnimationCurve.EASE_OUT),
            animate_opacity=ft.Animation(duration=480, curve=ft.AnimationCurve.EASE_OUT),
        )
        for size, color in zip(
            (12, 9, 15, 8),
            (ft.Colors.PINK_100, ft.Colors.LIGHT_BLUE_100, ft.Colors.YELLOW_100, ft.Colors.PURPLE_100),
        )
    ]
    bubble_stage = ft.Stack(
        width=340,
        height=100,
        controls=[
            ft.Row(left=0, top=14, spacing=8, controls=tile_boxes),
            *bubbles,
        ],
    )

    status_text = ft.Text("", color=ft.Colors.GREY_800)
    stats_text = ft.Text("", color=ft.Colors.GREY_700)
    quiz_feedback = ft.Text("", color=ft.Colors.GREY_800)
    next_button = ft.Button(
        content=ft.Text("Next Step", color=ft.Colors.GREY_900),
        icon=ft.Icons.ARROW_FORWARD,
        bgcolor=ft.Colors.PINK_100,
        on_click=advance,
    )

    demo = ft.Column(
        tight=True,
        spacing=12,
        controls=[
            bubble_stage,
            status_text,
            stats_text,
            ft.Row(
                wrap=True,
                spacing=10,
                controls=[
                    next_button,
                    ft.OutlinedButton(
                        content=ft.Text("Start Over"),
                        icon=ft.Icons.REPLAY,
                        on_click=reset,
                    ),
                ],
            ),
        ],
    )

    quiz_content = ft.Column(
        tight=True,
        spacing=10,
        controls=[
            ft.Text("Sorting in ascending order: what should you do when neighbors are 7 and 2?"),
            ft.Row(
                wrap=True,
                spacing=10,
                controls=[
                    ft.Button(
                        content=ft.Text("Swap them", color=ft.Colors.GREY_900),
                        bgcolor=ft.Colors.PINK_100,
                        on_click=lambda: answer_quiz(True),
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Keep the order"),
                        on_click=lambda: answer_quiz(False),
                    ),
                ],
            ),
            quiz_feedback,
        ],
    )

    page.add(
        ft.Column(
            spacing=14,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                ft.Container(
                    expand=True,
                    padding=20,
                    border_radius=22,
                    bgcolor=ft.Colors.LIGHT_BLUE_100,
                    content=ft.Column(
                        tight=True,
                        spacing=8,
                        controls=[
                            ft.Text("🍬 SORTING LAB", size=15, color=ft.Colors.GREY_700),
                            ft.Text("Bubble Sort", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_900),
                            ft.Text("Watch the number bubbles pop, swap, and float into order!"),
                        ],
                    ),
                ),
                section(
                    "How It Works",
                    "Scan from left to right and compare neighboring values. If the left value is larger, swap them. At the end of each pass, the largest unsorted value has moved to the right.",
                    ft.Colors.YELLOW_100,
                    ft.Text(
                        "Remember: Compare neighbors · Swap if left is larger · Largest moves right",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_900,
                    ),
                ),
                section(
                    "Try It Step by Step",
                    "The highlighted values are being compared. Click Next Step to continue and watch little bubbles float up.",
                    ft.Colors.LIGHT_GREEN_100,
                    demo,
                ),
                section(
                    "Quick Check",
                    "Test your understanding of the swap rule.",
                    ft.Colors.PURPLE_100,
                    quiz_content,
                ),
            ],
        )
    )

    refresh()


ft.run(main)
