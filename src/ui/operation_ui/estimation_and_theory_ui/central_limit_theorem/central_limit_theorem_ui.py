
        html_formul = f"""
            <table align="center" cellpadding="0" cellspacing="0">
                <tr>
                    <td valign="middle">
                        <span style="text-decoration: overline;">X</span> &asymp; <i>N</i>
                    </td>
                    
                    <td valign="middle" style="font-size: 60px; font-weight: 300; padding-bottom: 10px;">
                        (
                    </td>
                    
                    <td valign="middle" >
                        {self.variable_1_display} ,
                    </td>
                    
                    <td valign="middle">
                        <table cellpadding="0" cellspacing="0">
                            <tr>
                                <td align="center" style="border-bottom: 2px solid currentColor;">
                                    {self.variable_2_display}
                                </td>
                            </tr>
                            <tr>
                                <td align="center" >
                                    {self.variable_3_display}
                                </td>
                            </tr>
                        </table>
                    </td>

                    <td valign="middle" style="font-size: 60px; font-weight: 300; padding-bottom: 10px; padding-left: 5px;">
                        )
                    </td>

                    <td valign="middle" style="padding-left: 10px;">
                        = {self.current_result}
                    </td>
                </tr>
            </table>
        """
        self.dynamic_formula.setText(html_formul)

