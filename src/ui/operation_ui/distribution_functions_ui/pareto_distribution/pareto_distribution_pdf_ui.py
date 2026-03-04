
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle" style="padding-right: 15px;">
                        <i>f({self.variable_3_display})</i> = 
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 3px solid currentColor; padding: 0 10px 5px 10px;">
                                    <table cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td valign="middle">{self.variable_1_display} {self.variable_2_display}</td>
                                            <td valign="top" style="font-size: 22px; padding-bottom: 15px;">{self.variable_1_display}</td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr>
                                <td align="center" style="padding: 5px 10px 0 10px;">
                                    <table cellpadding="0" cellspacing="0">
                                        <tr>
                                            <td valign="middle">{self.variable_3_display}</td>
                                            <td valign="top" style="font-size: 22px; padding-bottom: 15px;">{self.variable_1_display}+1</td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="padding-left: 25px; font-size: 32px;">
                        , <i>{self.variable_3_display}</i> &ge; <i>{self.variable_2_display}</i>
                    </td>

                    <td valign="middle" style="padding-left: 30px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)


        