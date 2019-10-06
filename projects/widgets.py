from django.forms import DateTimeInput

class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = 'projects/widgets/xdsoft_datetimepicker.html'