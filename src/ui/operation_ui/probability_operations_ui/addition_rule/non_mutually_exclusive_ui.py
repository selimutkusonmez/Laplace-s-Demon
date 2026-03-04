        html_formul = f"""
                    <table align="center" cellpadding="0" cellspacing="0">
                        <tr>
                            <td valign="middle" style="padding-right: 10px;">
                                <i>P(A &cup; B)</i> = 
                            </td>
                            <td valign="middle" align="center">
                                {self.variable_1_display} + {self.variable_2_display} - {self.variable_3_display}
                            </td>
                            <td valign="middle" style="padding-left: 10px;">
                                = {self.current_result}
                            </td>
                        </tr>
                    </table>
                    """
        self.dynamic_formula.setText(html_formul)

