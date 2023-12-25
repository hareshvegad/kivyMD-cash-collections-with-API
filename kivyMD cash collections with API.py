from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.label import MDLabel
from datetime import datetime
import json
from kivy.clock import Clock

# Your payment methods and data
payment_methods = ["cash", "cheque", "gpay", "neft/imps", "paytm", "phonepay"]
payment_api = [
    {
        "shopID": "1",
        "shop_name": "Title_1",
        "outstanding" : "235",
        "payment_method": ["cheque", "paytm", "phonepay"],
        "payment_amount": ["1500", "25000", "15400"]
    }
]


class PaymentMethodsApp(MDApp):
    def build(self):
        # Create a BoxLayout for the shop name and outstanding labels
        shop_info_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50, spacing=10, padding=10)

        # Add a label for the shop's name
        shop_name_value_label = MDLabel(text=payment_api[0]["shop_name"])
        shop_info_layout.add_widget(shop_name_value_label)

        # Add a label for the outstanding amount
        outstanding_value_label = MDLabel(text="₹" + payment_api[0]["outstanding"],halign="right")
        shop_info_layout.add_widget(outstanding_value_label)
            
        # Create a BoxLayout for the main screen with a vertical orientation
        main_layout = BoxLayout(orientation='vertical',padding="10dp",size_hint=(1, 0.92),pos_hint={"top": 0.92})

        # Create a ScrollView
        payment_scrollview = MDScrollView()
        
        # Create a GridLayout for displaying payment methods (60% of the screen)
        payment_layout = MDGridLayout(cols=2, padding=10, spacing=10)
        
        # Add headers for Payment Method and Amount
        payment_layout.add_widget(MDLabel(text="Payment Method", theme_text_color="Primary",bold=2))
        payment_layout.add_widget(MDLabel(text="Amount",theme_text_color="Primary",bold=2))

        # Iterate through payment methods
        for method in payment_methods:
            # Create a label for the payment method
            method_label = MDLabel(text=method, theme_text_color="Secondary")
            payment_layout.add_widget(method_label)

            # Create a label for the amount
            amount_label = MDLabel(text="", theme_text_color="Secondary")

            # Check if the current method exists in payment_api
            for data in payment_api:
                if method in data["payment_method"]:
                    # Set text color to Primary
                    method_label.theme_text_color = "Primary"
                    amount_index = data["payment_method"].index(method)
                    amount_label.theme_text_color = "Primary"
                    amount_label.text = data["payment_amount"][amount_index]
                    break

            payment_layout.add_widget(amount_label)

        # Calculate the required sizes based on percentages
        payment_layout.size_hint = (1, 0.7)  # 70% of the screen
        
        # Add the payment_layout to the ScrollView
        payment_scrollview.add_widget(payment_layout)

        # Add the shop_info_layout and payment_layout to the main layout
        main_layout.add_widget(shop_info_layout)
        main_layout.add_widget(payment_scrollview)

        # Create a BoxLayout for the text field and buttons (30% of the screen)
        text_field_and_buttons_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.6), padding=10)

        # Create a text field for the reason with a grey background, initially disabled
        self.reason_textfield = TextInput(
            hint_text="Reason",
            multiline=True,
            background_color=(0.9, 0.9, 0.9, 1),  # Grey background color
            disabled=True,
        )
        
        # Create a "Submit" button (initially disabled)
        submit_button = MDRaisedButton(
            text="Submit",
            md_bg_color=(1, 0.5, 0, 1),
            on_release=self.rejected_submit_approval,
            disabled=True,
        )

        # Function to enable the "Submit" button when the reason text is filled
        def check_reason_text(instance, value):
            submit_button.disabled = not bool(value)
            approve_button.disabled = bool(value)

        self.reason_textfield.bind(text=check_reason_text)
    
        # Add the text field to the layout
        text_field_and_buttons_layout.add_widget(self.reason_textfield)

        # Create a BoxLayout for buttons
        button_box = MDBoxLayout(orientation='horizontal', size_hint=(1, None), height=50,spacing=15,padding=(100, 0))

        # Add buttons (Approve and Cancel) to the button box
        approve_button = MDRaisedButton(text="Approve",md_bg_color=(1, 0.5, 0, 1), on_release=self.show_approval_popup)
        cancel_button = MDFlatButton(text="Reject", on_release=self.show_cancellation_popup)
        button_box.add_widget(approve_button)
        button_box.add_widget(cancel_button)
        button_box.add_widget(submit_button)
        

        # Add the button box to the layout
        text_field_and_buttons_layout.add_widget(button_box)

        # Add the text field and buttons layout to the main layout
        main_layout.add_widget(text_field_and_buttons_layout)

        return main_layout
    
    def rejected_submit_approval(self, instance):
        # Get the current date and time
        now = datetime.now()
        
        # Format the date and time as a string
        current_datetime = now.strftime('%d-%m-%Y %H:%M:%S')

        # Create the rejection data including shopID and shop_name
        rejected_data = {
            "shopID": payment_api[0]["shopID"],
            "shop_name": payment_api[0]["shop_name"],
            "status": "Rejected",
            "datetime": current_datetime,
            "reason": self.reason_textfield.text,
        }

        # Convert the dictionary to JSON format
        rejected_data_json = json.dumps(rejected_data)

        # Save or send the rejected data to your API here
        print(rejected_data_json)

    def show_approval_popup(self, instance):
        # Create a custom MDDialog without any buttons
        methods_to_approve = payment_api[0]["payment_method"]  # Replace with the methods you want to approve

        # Get the current date and time
        current_datetime = datetime.now()

        # Create an API data structure to save the approved data
        approval_data = {
            "shopID": payment_api[0]["shopID"],
            "shop_name": payment_api[0]["shop_name"],
            "status": "Approved",
            "date": current_datetime.strftime('%d-%m-%Y %H:%M:%S'),  # Format the date and time as needed
            "approved_methods": methods_to_approve,        }

        # Find the corresponding amounts for the approved methods
        approved_amounts = []
        for method_to_approve in methods_to_approve:
            for data in payment_api:
                if method_to_approve in data["payment_method"]:
                    amount_index = data["payment_method"].index(method_to_approve)
                    approved_amounts.append({
                        "method": method_to_approve,
                        "amount": data['payment_amount'][amount_index]
                    })

        if approved_amounts:
            # Add approved amounts to the approval data
            approval_data["approved_amounts"] = approved_amounts

        # Convert the approval data to JSON or any other required format
        approval_data_json = json.dumps(approval_data)
        print(approval_data_json)

        # You can save or send the data as needed (e.g., send it to an API or save it to a file)
        
        # Now, display the approval information in the dialog
        approval_info = "Payment Approved:\nMethods: " + ", ".join(methods_to_approve) 

        
        popup = MDDialog(
            title="Approval",
            text=approval_info,
        )

        # Create a BoxLayout with a vertical orientation for the dialog's content
        content_box = BoxLayout(orientation="vertical")

        # Add a label to display the remaining time
        time_label = Label(halign="center", valign='middle')
        content_box.add_widget(time_label)

        # Add the content_box to the popup
        popup.content_cls = content_box

        # Remove the dismiss event (tap outside the dialog) to prevent closing
        popup.auto_dismiss = False

        # Open the custom dialog
        popup.open()

        # Function to update the time label and dismiss the dialog after 5 seconds
        time_remaining = 5  # Initial time remaining in seconds
        def update_time_label(interval):
            nonlocal time_remaining
            if time_remaining > 0:
                time_label.text = f"Time remaining: {time_remaining} seconds"
                time_remaining -= 1
            else:
                popup.dismiss()
        
        # Schedule the countdown to update the time label and dismiss the dialog
        Clock.schedule_interval(update_time_label, 1)
        
    def show_cancellation_popup(self, instance):
        # Create a custom MDDialog for cancellation       
        cancel_popup = MDDialog(
            content_cls=MDBoxLayout(orientation="vertical",size_hint_y=None,height="150dp",spacing=20), 
            title="Cancellation",
            type="custom", 
            ) 
        
        # Create a text input field for the cancellation reason
        cancel_reason_textfield = TextInput(
            hint_text="Reason for cancellation",
            multiline=True,
            background_color=(0.9, 0.9, 0.9, 1),  
        )

        # Function to print the cancellation reason
        def print_cancellation_reason(instance):
            self.reason_textfield.text = "Cancellation Reason : " + cancel_reason_textfield.text
            cancel_popup.dismiss()
            
        # Create an OK button to confirm the cancellation
        ok_button = MDRaisedButton(
            text="OK",
            pos_hint={'center_x': 0.5},
            on_release=print_cancellation_reason
        )

        # Add the text input and OK button to the popup's content
        cancel_popup.content_cls.add_widget(cancel_reason_textfield)
        cancel_popup.content_cls.add_widget(ok_button)

        # Open the custom cancellation dialog
        cancel_popup.open()

if __name__ == '__main__':
    PaymentMethodsApp().run()
