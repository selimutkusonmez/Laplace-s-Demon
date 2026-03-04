        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0" >
                <tr>
                    <td valign="middle" style="padding-right: 10px;">
                        <i>f({self.variable_1_display})</i> = 
                    </td>
                    
                    <td valign="middle" style="font-size: 150px; font-weight: lighter; padding-bottom: 8px;">
                        {{
                    </td>

                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0" style="font-size: 32px;">
                            <tr>
                                <td valign="middle" align="center">
                                    <table cellpadding="0" cellspacing="0">
                                        <tr><td align="center" style="border-bottom: 2px solid currentColor; padding: 0px 5px 2px 5px;">1</td></tr>
                                        <tr><td align="center" style="padding: 2px 5px 0px 5px;">{self.variable_3_display} &minus; {self.variable_2_display}</td></tr>
                                    </table>
                                </td>
                                <td valign="middle">,</td>
                                <td valign="middle" style="padding-left: 20px;">
                                    {self.variable_2_display} &le; {self.variable_1_display} &le; {self.variable_3_display}
                                </td>
                            </tr>
                            <tr>
                                <td valign="middle" align="center">0</td>
                                <td valign="middle">,</td>
                                <td valign="middle" style="padding-left: 20px;">
                                    other cases
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 35px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

 